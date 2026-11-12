import re

from llm_brand_visiblity_v2.schemas import BrandInput
from llm_brand_visiblity_v2.schemas import NormalizedPromptResponse
from llm_brand_visiblity_v2.schemas import ResolvedEntity
from llm_brand_visiblity_v2.schemas import EntityAssessment
from llm_brand_visiblity_v2.schemas import CitationMention
from llm_brand_visiblity_v2.schemas import ResponseAnalysis
from llm_brand_visiblity_v2.schemas import SentimentLabelEnum
from llm_brand_visiblity_v2.schemas import RecommendationStatusEnum
from llm_brand_visiblity_v2.schemas import ComparisonOutcomeEnum
from llm_brand_visiblity_v2.schemas import ResolutionStatusEnum
from llm_brand_visiblity_v2.schemas import CanonicalEntityTypeEnum


class ResponseAnalysisEngine:

    POSITIVE_WORDS = {
        "excellent", "great", "best", "good", "better",
        "reliable", "effective", "recommended", "superior",
        "comfortable", "affordable", "impressive"
    }

    NEGATIVE_WORDS = {
        "bad", "poor", "worst", "worse", "expensive",
        "unreliable", "inferior", "disappointing",
        "uncomfortable", "avoid", "weak"
    }

    POSITIVE_RECOMMENDATION_PHRASES = {
        "recommend", "recommended", "best choice",
        "top choice", "ideal choice", "worth buying",
        "top pick", "should buy"
    }

    NEGATIVE_RECOMMENDATION_PHRASES = {
        "not recommend", "not recommended",
        "avoid", "stay away", "not worth buying",
        "poor choice"
    }

    def entity_sentiment(self, text: str) -> SentimentLabelEnum:

        words = re.findall(r"\b[\w'-]+\b", text.lower())

        positive_count = sum(
            word in self.POSITIVE_WORDS for word in words
        )

        negative_count = sum(
            word in self.NEGATIVE_WORDS for word in words
        )

        if positive_count > 0 and negative_count > 0:
            return SentimentLabelEnum.MIXED

        if positive_count > negative_count:
            return SentimentLabelEnum.POSITIVE

        if negative_count > positive_count:
            return SentimentLabelEnum.NEGATIVE

        return SentimentLabelEnum.NEUTRAL

    def recommendation_status(
        self,
        text: str
    ) -> RecommendationStatusEnum:

        text = text.lower()

        if any(
            phrase in text
            for phrase in self.NEGATIVE_RECOMMENDATION_PHRASES
        ):
            return RecommendationStatusEnum.NOT_RECOMMENDED

        if any(
            phrase in text
            for phrase in self.POSITIVE_RECOMMENDATION_PHRASES
        ):
            return RecommendationStatusEnum.RECOMMENDED

        return RecommendationStatusEnum.NOT_STATED

    def comparison_outcome(
        self,
        text: str,
        target_brand: str,
        entity: ResolvedEntity
    ) -> ComparisonOutcomeEnum:

        text_lower = text.lower()
        target_lower = target_brand.lower()

        if (
            entity.resolution_status != ResolutionStatusEnum.RESOLVED
            or entity.canonical_type != CanonicalEntityTypeEnum.COMPETITOR
        ):
            return ComparisonOutcomeEnum.NOT_APPLICABLE

        competitor_lower = entity.canonical_name.lower()

        if target_lower not in text_lower or competitor_lower not in text_lower:
            return ComparisonOutcomeEnum.NOT_APPLICABLE

        if re.search(r"\b(as good as|equally good|on par with)\b", text_lower):
            return ComparisonOutcomeEnum.EQUAL

        # Identify explicit preference statements
        preference_match = re.search(
            r"(?:prefer|preferred)\s+(.+?)\s+(?:over|to)\s+(.+)",
            text_lower
        )

        if preference_match:
            preferred = preference_match.group(1)
            if target_lower in preferred:
                return ComparisonOutcomeEnum.TARGET_FAVORED
            if competitor_lower in preferred:
                return ComparisonOutcomeEnum.COMPETITOR_FAVORED

        # Identify explicit better/worse comparisons
        for phrase in ("better than", "superior to", "outperforms"):
            if phrase in text_lower:
                left, right = text_lower.split(phrase, 1)

                if target_lower in left and competitor_lower in right:
                    return ComparisonOutcomeEnum.TARGET_FAVORED

                if competitor_lower in left and target_lower in right:
                    return ComparisonOutcomeEnum.COMPETITOR_FAVORED

        for phrase in ("worse than", "inferior to", "underperforms"):
            if phrase in text_lower:
                left, right = text_lower.split(phrase, 1)

                if target_lower in left and competitor_lower in right:
                    return ComparisonOutcomeEnum.COMPETITOR_FAVORED

                if competitor_lower in left and target_lower in right:
                    return ComparisonOutcomeEnum.TARGET_FAVORED

        if re.search(r"\b(vs\.?|versus|compared with|compared to)\b", text_lower):
            return ComparisonOutcomeEnum.COMPARISON_MENTIONED

        return ComparisonOutcomeEnum.NOT_APPLICABLE

    def ranking_position(
        self,
        text: str,
        entity_name: str
    ) -> int | None:

        escaped_name = re.escape(entity_name)

        patterns = [
            rf"{escaped_name}\s*(?:is\s+)?(?:ranked|rank)\s*(?:at|number|#)?\s*(\d+)",
            rf"(?:ranked|rank)\s*(?:at|number|#)?\s*(\d+)\s*(?:is\s+)?{escaped_name}",
            rf"{escaped_name}\s*(?:is\s+)?#\s*(\d+)",
            rf"#\s*(\d+)\s*{escaped_name}"
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

    def extract_citations(
        self,
        response_text: str
    ) -> list[CitationMention]:

        citations: list[CitationMention] = []

        url_pattern = r"https?://[^\s<>\]\)\"']+"

        for match in re.finditer(url_pattern, response_text):

            url = match.group().rstrip(".,;:")

            citations.append(
                CitationMention(
                    url=url,
                    start_position=match.start(),
                    end_position=match.start() + len(url)
                )
            )

        return citations

    def analyze_responses(
        self,
        normalized_responses: list[NormalizedPromptResponse],
        resolved_entities: list[ResolvedEntity],
        brand_input: BrandInput
    ) -> list[ResponseAnalysis]:

        analysis_results: list[ResponseAnalysis] = []

        # Group resolved entities by response ID
        entities_by_response: dict[int, list[ResolvedEntity]] = {}

        for entity in resolved_entities:

            response_id = entity.source_entity.prompt_response.response_id

            entities_by_response.setdefault(
                response_id, []
            ).append(entity)

        for response in normalized_responses:

            response_entities = entities_by_response.get(
                response.response_id, []
            )

            entity_assessments: list[EntityAssessment] = []

            # Analyse each entity within its sentence
            for entity in response_entities:

                start = entity.source_entity.start_position
                end = entity.source_entity.end_position

                # Extract the sentence containing this entity
                sentence = self.sentence_for_span(
                    response.response,
                    start
                )

                sentiment = self.entity_sentiment(sentence)

                recommendation = self.recommendation_status(sentence)

                comparison = self.comparison_outcome(
                    sentence,
                    brand_input.brand_name,
                    entity
                )

                rank = self.ranking_position(
                    sentence,
                    entity.canonical_name or entity.source_entity.entity_text
                )

                entity_assessments.append(
                    EntityAssessment(
                        entity=entity,
                        sentiment=sentiment,
                        recommendation=recommendation,
                        comparison=comparison,
                        rank_position=rank
                    )
                )

            citations = self.extract_citations(response.response)

            analysis_results.append(
                ResponseAnalysis(
                    response_id=response.response_id,
                    prompt_response=response,
                    entity_assessments=entity_assessments,
                    citations=citations
                )
            )

        return analysis_results

    def sentence_for_span(self, text: str, position: int) -> str:
        sentence_start = 0

        for match in re.finditer(r"[.!?](?:\s+|$)", text):
            sentence_end = match.end()

            if sentence_start <= position < sentence_end:
                return text[sentence_start:sentence_end].strip()

            sentence_start = sentence_end

        return text[sentence_start:].strip()
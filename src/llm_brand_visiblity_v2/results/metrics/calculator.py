from dataclasses import dataclass, field
from llm_brand_visiblity_v2.schemas import (
    ResponseAnalysis,
    CanonicalEntityTypeEnum,
    SentimentLabelEnum,
    RecommendationStatusEnum,
    BrandInput,
)

@dataclass
class EntityMetrics:
    canonical_name: str
    entity_type: CanonicalEntityTypeEnum
    total_mentions: int = 0
    prompts_with_mention: int = 0
    mention_rate: float = 0.0          # % of total prompts mentioning this entity
    share_of_voice: float = 0.0        # % of all mentions across entities
    recommendation_count: int = 0
    recommendation_rate: float = 0.0   # % of prompt responses recommending this entity
    average_rank: float | None = None
    mrr: float = 0.0                   # Mean Reciprocal Rank across prompts
    positive_sentiment_count: int = 0
    neutral_sentiment_count: int = 0
    negative_sentiment_count: int = 0
    net_sentiment_score: float = 0.0   # (pos - neg) / total_mentions if total > 0 else 0.0


@dataclass
class MetricsReport:
    total_prompts_analyzed: int
    target_brand: str
    entity_metrics: dict[str, EntityMetrics] = field(default_factory=dict)
    brand_citations_count: int = 0
    competitor_citations_count: int = 0
    all_citations: list[str] = field(default_factory=list)


class MetricsCalculator:
    """Calculates brand visibility, Share of Voice (SoV), MRR, and sentiment metrics."""

    def calculate_metrics(
        self,
        analyses: list[ResponseAnalysis],
        brand_input: BrandInput,
    ) -> MetricsReport:
        total_prompts = len(analyses)
        report = MetricsReport(
            total_prompts_analyzed=total_prompts,
            target_brand=brand_input.brand_name,
        )

        # Track entities: target brand + competitors
        entities_to_track: dict[str, CanonicalEntityTypeEnum] = {
            brand_input.brand_name: CanonicalEntityTypeEnum.BRAND
        }
        if brand_input.competitors:
            for comp in brand_input.competitors:
                entities_to_track[comp] = CanonicalEntityTypeEnum.COMPETITOR

        for name, ent_type in entities_to_track.items():
            report.entity_metrics[name] = EntityMetrics(
                canonical_name=name,
                entity_type=ent_type,
            )

        total_mentions_all = 0
        rank_sum: dict[str, list[int]] = {name: [] for name in entities_to_track}
        rr_sum: dict[str, float] = {name: 0.0 for name in entities_to_track}

        for analysis in analyses:
            # Collect unique mentions per prompt to calculate prompt-level mention rates
            seen_in_prompt: set[str] = set()
            recommended_in_prompt: set[str] = set()

            for assessment in analysis.entity_assessments:
                canonical_name = assessment.entity.canonical_name
                if not canonical_name or canonical_name not in report.entity_metrics:
                    continue

                metric = report.entity_metrics[canonical_name]
                metric.total_mentions += 1
                total_mentions_all += 1
                seen_in_prompt.add(canonical_name)

                # Sentiment
                if assessment.sentiment == SentimentLabelEnum.POSITIVE:
                    metric.positive_sentiment_count += 1
                elif assessment.sentiment == SentimentLabelEnum.NEGATIVE:
                    metric.negative_sentiment_count += 1
                elif assessment.sentiment == SentimentLabelEnum.NEUTRAL:
                    metric.neutral_sentiment_count += 1

                # Recommendation
                if assessment.recommendation == RecommendationStatusEnum.RECOMMENDED:
                    recommended_in_prompt.add(canonical_name)

                # Rank & Reciprocal Rank
                if assessment.rank_position is not None and assessment.rank_position > 0:
                    rank_sum[canonical_name].append(assessment.rank_position)

            # Update per-prompt statistics
            for name in seen_in_prompt:
                report.entity_metrics[name].prompts_with_mention += 1
            for name in recommended_in_prompt:
                report.entity_metrics[name].recommendation_count += 1

            # Reciprocal rank per prompt (1 / rank if present, else 0)
            for name in entities_to_track:
                # Find best rank in this prompt
                ranks_in_this_prompt = [
                    a.rank_position
                    for a in analysis.entity_assessments
                    if a.entity.canonical_name == name and a.rank_position is not None and a.rank_position > 0
                ]
                if ranks_in_this_prompt:
                    best_rank = min(ranks_in_this_prompt)
                    rr_sum[name] += 1.0 / best_rank

            # Citations
            for citation in analysis.citations:
                report.all_citations.append(citation.url)
                if brand_input.brand_name.lower() in citation.url.lower():
                    report.brand_citations_count += 1
                else:
                    report.competitor_citations_count += 1

        # Final aggregate computations
        for name, metric in report.entity_metrics.items():
            if total_prompts > 0:
                metric.mention_rate = round((metric.prompts_with_mention / total_prompts) * 100, 2)
                metric.recommendation_rate = round((metric.recommendation_count / total_prompts) * 100, 2)
                metric.mrr = round(rr_sum[name] / total_prompts, 4)

            if total_mentions_all > 0:
                metric.share_of_voice = round((metric.total_mentions / total_mentions_all) * 100, 2)

            if rank_sum[name]:
                metric.average_rank = round(sum(rank_sum[name]) / len(rank_sum[name]), 2)

            if metric.total_mentions > 0:
                metric.net_sentiment_score = round(
                    (metric.positive_sentiment_count - metric.negative_sentiment_count) / metric.total_mentions,
                    2,
                )

        return report


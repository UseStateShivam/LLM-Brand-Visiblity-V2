
import spacy
from spacy.matcher import PhraseMatcher

from llm_brand_visiblity_v2.schemas import ExtractionMethodEnum
from llm_brand_visiblity_v2.schemas import ExtractedEntity
from llm_brand_visiblity_v2.schemas import BrandInput
from llm_brand_visiblity_v2.schemas import NormalizedPromptResponse


class EntityExtraction:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def entity_extraction(
        self,
        normalized_responses: list[NormalizedPromptResponse],
        brand_input: BrandInput
    ) -> list[ExtractedEntity]:

        list_of_extracted_entities: list[ExtractedEntity] = []

        # Build entity dictionary
        entity_dictionary = {
            "BRAND": [brand_input.brand_name],
            "COMPETITOR": brand_input.competitors or [],
            "PRODUCT": brand_input.products or [],
            "SERVICE": brand_input.services or []
        }

        # Initialize dictionary matcher
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")

        # Register dictionary patterns
        for entity_type, entity_names in entity_dictionary.items():

            patterns = [
                self.nlp.make_doc(entity_name)
                for entity_name in entity_names
            ]

            if patterns:
                matcher.add(entity_type, patterns)

        # Process each prompt-response independently
        for response in normalized_responses:

            doc = self.nlp(response.response)

            # Dictionary-based extraction
            dictionary_matches = []

            for match_id, start, end in matcher(doc):

                entity = doc[start:end]
                entity_type = self.nlp.vocab.strings[match_id]

                dictionary_matches.append(
                    (entity, entity_type)
                )

            # NER extraction
            for entity in doc.ents:

                # Avoid duplicate/overlapping NER mentions
                # when dictionary matching identifies a known entity.
                overlaps_dictionary = any(
                    entity.start_char < matched_entity.end_char
                    and entity.end_char > matched_entity.start_char
                    for matched_entity, _ in dictionary_matches
                )

                if overlaps_dictionary:
                    continue

                extracted_entity = ExtractedEntity(
                    prompt_response=response,
                    entity_text=entity.text,
                    entity_type=entity.label_,
                    start_position=entity.start_char,
                    end_position=entity.end_char,
                    extraction_method=ExtractionMethodEnum.NER
                )

                list_of_extracted_entities.append(extracted_entity)

            # Add dictionary-based entities
            for entity, entity_type in dictionary_matches:

                extracted_entity = ExtractedEntity(
                    prompt_response=response,
                    entity_text=entity.text,
                    entity_type=entity_type,
                    start_position=entity.start_char,
                    end_position=entity.end_char,
                    extraction_method=ExtractionMethodEnum.DICT
                )

                list_of_extracted_entities.append(extracted_entity)

        return list_of_extracted_entities
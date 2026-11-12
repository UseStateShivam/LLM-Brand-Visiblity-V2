from llm_brand_visiblity_v2.schemas import BrandInput
from llm_brand_visiblity_v2.schemas import ExtractedEntity
from llm_brand_visiblity_v2.schemas import ResolvedEntity
from llm_brand_visiblity_v2.schemas import CanonicalEntityTypeEnum
from llm_brand_visiblity_v2.schemas import ResolutionStatusEnum

class EntityResolution:

    def entity_resolution(
        self,
        extracted_entities: list[ExtractedEntity],
        brand_input: BrandInput
    ) -> list[ResolvedEntity]:

        resolved_entities: list[ResolvedEntity] = []

        # Build canonical entity dictionary
        entity_dictionary = {
            CanonicalEntityTypeEnum.BRAND: [brand_input.brand_name],
            CanonicalEntityTypeEnum.COMPETITOR: brand_input.competitors or [],
            CanonicalEntityTypeEnum.PRODUCT: brand_input.products or [],
            CanonicalEntityTypeEnum.SERVICE: brand_input.services or []
        }

        # Create case-insensitive lookup
        entity_lookup = {}

        for entity_type, names in entity_dictionary.items():
            for name in names:
                entity_lookup[name.casefold()] = (name, entity_type)

        for extracted_entity in extracted_entities:

            matched_entity = entity_lookup.get(
                extracted_entity.entity_text.casefold()
            )

            if matched_entity is not None:

                canonical_name, canonical_type = matched_entity

                resolved_entity = ResolvedEntity(
                    source_entity=extracted_entity,
                    canonical_name=canonical_name,
                    canonical_type=canonical_type,
                    resolution_status=ResolutionStatusEnum.RESOLVED
                )

            else:

                resolved_entity = ResolvedEntity(
                    source_entity=extracted_entity,
                    canonical_name=None,
                    canonical_type=None,
                    resolution_status=ResolutionStatusEnum.UNRESOLVED
                )

            resolved_entities.append(resolved_entity)

        return resolved_entities

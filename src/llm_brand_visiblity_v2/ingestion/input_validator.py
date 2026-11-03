from pydantic import ValidationError
from llm_brand_visiblity_v2.schemas import BrandInput

def validate_and_build_input(raw_map):
    try:
        brand_validated_model = BrandInput.model_validate(raw_map)
    except ValidationError as e:
        raise e

    return brand_validated_model
from llm_brand_visiblity_v2.ingestion.input_validator import validate_and_build_input
from llm_brand_visiblity_v2.ingestion.input_reader import read_input

def run_ingestion_pipeline():
    raw_map = read_input()
    validated_input_model = validate_and_build_input(raw_map)

    return validated_input_model
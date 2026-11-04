from llm_brand_visiblity_v2.core.prompt_gen.builder import BuildPrompts
from llm_brand_visiblity_v2.ingestion.pipeline import run_ingestion_pipeline

def test_ingestion_and_prompt_gen():
    input_model = run_ingestion_pipeline()
    prompt_builder = BuildPrompts(brand_input= input_model)

    print(prompt_builder.build_prompt_list())

if __name__ == "__main__":
    test_ingestion_and_prompt_gen()
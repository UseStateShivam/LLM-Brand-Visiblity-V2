from pydantic import ValidationError
from llm_brand_visiblity_v2.schemas import BrandInput


def website_input_validation():
    try:
        BrandInput(brand_name="", niche="Search Engine", website="https://google.com")
    except ValidationError as e:
        print(e)

website_input_validation()
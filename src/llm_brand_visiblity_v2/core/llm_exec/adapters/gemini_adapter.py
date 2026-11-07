import os
from google import genai
from datetime import timezone
from datetime import datetime
from dotenv import load_dotenv
from llm_brand_visiblity_v2.schemas import Prompt
from llm_brand_visiblity_v2.schemas import TypeEnum
from llm_brand_visiblity_v2.schemas import IntentEnum
from llm_brand_visiblity_v2.schemas import ContextEnum
from llm_brand_visiblity_v2.schemas import AdapterResponse
from llm_brand_visiblity_v2.core.llm_exec.adapters.base_adapter import BaseAdapter

class GeminiAdapter(BaseAdapter):
    def __init__(self):
        load_dotenv()
        
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.client = client

    def execute(self, prompt: Prompt) -> AdapterResponse:
        response = self.client.models.generate_content(
            model = "gemini-3.5-flash",
            contents = prompt.content 
        )

        adapter_response = AdapterResponse(
            content= response.text, 
            input_tokens= response.usage_metadata.prompt_token_count, 
            output_tokens= response.usage_metadata.candidates_token_count, 
            total_tokens= response.usage_metadata.total_token_count, 
            finished_at= datetime.now(timezone.utc)
        )

        return adapter_response

if __name__ == "__main__":
    prompt = Prompt(
        prompt_id=1, 
        intent=IntentEnum.INFORMATIONAL, 
        context=ContextEnum.BRANDLEVEL, 
        prompt_type=TypeEnum.BRANDED, 
        content="What color is the sky?"
    )

    gemini_adapter_instance = GeminiAdapter()
    adp_res = gemini_adapter_instance.execute(prompt)
    print(adp_res)
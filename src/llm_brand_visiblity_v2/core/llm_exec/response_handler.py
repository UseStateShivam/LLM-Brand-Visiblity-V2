import uuid
from llm_brand_visiblity_v2.schemas import RawResult
from llm_brand_visiblity_v2.schemas import AdapterResponse

class ResponseHandler:
    def handle_response(self, adapter_response: AdapterResponse, attempt_id: int, sequence_number: int) -> RawResult:
        raw_result = RawResult(
            result_id= uuid.uuid4().int,
            attempt_id= attempt_id,
            sequence_number= sequence_number,
            content= adapter_response.content
        )

        return raw_result
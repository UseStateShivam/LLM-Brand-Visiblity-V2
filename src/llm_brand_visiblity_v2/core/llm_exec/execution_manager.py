import uuid
import time
from datetime import timezone
from datetime import datetime
from llm_brand_visiblity_v2.schemas import Prompt
from llm_brand_visiblity_v2.schemas import Attempt
from llm_brand_visiblity_v2.schemas import RawResult
from llm_brand_visiblity_v2.schemas import TypeEnum
from llm_brand_visiblity_v2.schemas import IntentEnum
from llm_brand_visiblity_v2.schemas import StatusEnum
from llm_brand_visiblity_v2.schemas import PromptExec
from llm_brand_visiblity_v2.schemas import ContextEnum
from llm_brand_visiblity_v2.core.llm_exec.response_handler import ResponseHandler
from llm_brand_visiblity_v2.core.llm_exec.adapters.gemini_adapter import GeminiAdapter

class ExecutionManager:
    def execute(self, prompts_list: list[Prompt]) -> tuple[list[Attempt], list[RawResult]]:
        raw_results = []
        attempts_list = []

        gemnini_adapter = GeminiAdapter()
        response_handler_instance = ResponseHandler()

        for i in range(len(prompts_list)):
            prompt = prompts_list[i]

            execution = PromptExec(
                prompt_id= prompt.prompt_id,
                execution_id= uuid.uuid4().int,
                provider= "Gemini",
                model= "gemini-3.5-flash"
            )

            attempt = Attempt(
                attempt_id= uuid.uuid4().int,
                execution_id= execution.execution_id,
                attempt_number= 1,
                started_at= datetime.now(timezone.utc)
            )

            start_time = time.perf_counter()
            
            try:
                adapter_response = gemnini_adapter.execute(prompt)
            except RuntimeError as e:
                print("Prompt with prompt_id =", prompt.prompt_id, "failed: ", e)
                attempt.status = StatusEnum.CLIENT_ERROR
            else:
                attempt.status = StatusEnum.SUCCESS
                attempt.input_tokens = adapter_response.input_tokens
                attempt.output_tokens = adapter_response.output_tokens
                attempt.total_tokens = adapter_response.total_tokens
                raw_result = response_handler_instance.handle_response(adapter_response, attempt.attempt_id, i)
                raw_results.append(raw_result)
            finally:
                attempt.response_code = None
                attempt.finished_at = datetime.now(timezone.utc)
                attempt.latency = time.perf_counter() - start_time
                attempts_list.append(attempt)

        return attempts_list, raw_results

if __name__ == "__main__":
    execution_manager = ExecutionManager()

    prompt = Prompt(
        prompt_id= 1,
        intent= IntentEnum.BUYING,
        context= ContextEnum.BRANDLEVEL,
        prompt_type= TypeEnum.BRANDED,
        content= "Which nike shoe shall I buy for running?"
    )

    prompts_list = [prompt]

    print(execution_manager.execute(prompts_list))
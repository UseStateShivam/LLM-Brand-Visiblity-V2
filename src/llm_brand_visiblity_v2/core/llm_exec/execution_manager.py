import uuid
import time
from datetime import timezone
from datetime import datetime
from google.genai import errors
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
    def execute(self, prompts_list: list[Prompt]) -> tuple[list[PromptExec], list[Attempt], list[RawResult]]:
        raw_results = []
        prompt_executions = []
        attempts_list = []
        failed_prompts_metadata = []

        passes = 0

        gemnini_adapter = GeminiAdapter()
        response_handler_instance = ResponseHandler()

        def prompt_looping(prompts_list = None, failed_prompts_list = None):
            working_list = []

            if passes == 0:
                working_list = prompts_list
            else:
                working_list = failed_prompts_list

            for i in range(len(working_list)):
                prompt: Prompt
                execution_id: int
                sequence_number: int

                if passes != 0:
                    prompt, execution_id, sequence_number = working_list[i]
                    attempt = Attempt(
                        attempt_id= uuid.uuid4().int,
                        execution_id= execution_id,
                        attempt_number= passes+1,
                        started_at= datetime.now(timezone.utc)
                    )
                else:
                    prompt = prompts_list[i]
                    execution = PromptExec(
                        prompt_id= prompt.prompt_id,
                        execution_id= uuid.uuid4().int,
                        provider= "Gemini",
                        model= "gemini-3.5-flash"
                    )
                    prompt_executions.append(execution)
                    attempt = Attempt(
                        attempt_id= uuid.uuid4().int,
                        execution_id= execution.execution_id,
                        attempt_number= passes+1,
                        started_at= datetime.now(timezone.utc)
                    )
                    sequence_number = i

                start_time = time.perf_counter()
                
                try:
                    adapter_response = gemnini_adapter.execute(prompt)
                except errors.ClientError as e:
                        attempt.status = StatusEnum.CLIENT_ERROR
                        print("Prompt with prompt_id =", prompt.prompt_id, "failed: ", e)
                        if passes == 0:
                            failed_prompts_metadata.append((prompt, execution.execution_id, i))
                except errors.ServerError as e:
                        attempt.status = StatusEnum.SERVER_ERROR
                        print("Prompt with prompt_id =", prompt.prompt_id, "failed: ", e)
                        if passes == 0:
                            failed_prompts_metadata.append((prompt, execution.execution_id, i))
                except TimeoutError as e:
                        attempt.status = StatusEnum.TIMEOUT
                        print("Prompt with prompt_id =", prompt.prompt_id, "failed: ", e)
                        if passes == 0:
                            failed_prompts_metadata.append((prompt, execution.execution_id, i))
                except errors.APIError as e:
                        attempt.status = StatusEnum.CLIENT_ERROR
                        print("Prompt with prompt_id =", prompt.prompt_id, "failed: ", e)
                        if passes == 0:
                            failed_prompts_metadata.append((prompt, execution.execution_id, i))
                else:
                    attempt.status = StatusEnum.SUCCESS
                    attempt.input_tokens = adapter_response.input_tokens
                    attempt.output_tokens = adapter_response.output_tokens
                    attempt.total_tokens = adapter_response.total_tokens
                    raw_result = response_handler_instance.handle_response(adapter_response, attempt.attempt_id, sequence_number)
                    raw_results.append(raw_result)
                finally:
                    attempt.response_code = None
                    attempt.finished_at = datetime.now(timezone.utc)
                    attempt.latency = time.perf_counter() - start_time
                    attempts_list.append(attempt)

        prompt_looping(prompts_list=prompts_list)
        passes += 1
        prompt_looping(failed_prompts_list=failed_prompts_metadata)

        return prompt_executions, attempts_list, raw_results

if __name__ == "__main__":
    execution_manager = ExecutionManager()

    prompts_list = [
    # Prompt 1: succeeds on first attempt
        Prompt(
            prompt_id=1,
            intent=IntentEnum.BUYING,
            context=ContextEnum.BRANDLEVEL,
            prompt_type=TypeEnum.BRANDED,
            content="Which Nike running shoe is best for beginners?"
        ),

        # Prompt 2: succeeds on first attempt
        Prompt(
            prompt_id=2,
            intent=IntentEnum.INFORMATIONAL,
            context=ContextEnum.PRODUCTLEVEL,
            prompt_type=TypeEnum.BRANDED,
            content="What are the features of Nike Pegasus running shoes?"
        ),

        # Prompt 3: fails once, succeeds on retry
        Prompt(
            prompt_id=3,
            intent=IntentEnum.COMPARISON,
            context=ContextEnum.PRODUCTLEVEL,
            prompt_type=TypeEnum.COMPETITOR,
            content="Compare Nike Pegasus with Adidas Ultraboost."
        ),

        # Prompt 4: fails on both attempts
        Prompt(
            prompt_id=4,
            intent=IntentEnum.BUYING,
            context=ContextEnum.PRODUCTLEVEL,
            prompt_type=TypeEnum.UNBRANDED,
            content="Which running shoes are best for daily road running?"
        )
    ]

    print(execution_manager.execute(prompts_list))
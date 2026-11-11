import uuid
import time
from datetime import timezone, datetime
from google.genai import errors
from llm_brand_visiblity_v2.schemas import (
    Prompt,
    Attempt,
    RawResult,
    StatusEnum,
    PromptExec,
)
from llm_brand_visiblity_v2.core.llm_exec.response_handler import ResponseHandler
from llm_brand_visiblity_v2.core.llm_exec.adapters.gemini_adapter import GeminiAdapter

class ExecutionManager:
    def execute(
        self,
        prompts_list: list[Prompt]
    ) -> list[tuple[PromptExec, list[Attempt], RawResult | None]]:

        list_of_tuples = []

        gemini_adapter = GeminiAdapter()
        response_handler_instance = ResponseHandler()

        for sequence_number, prompt in enumerate(prompts_list):

            execution = PromptExec(
                prompt_id=prompt.prompt_id,
                execution_id=uuid.uuid4().int,
                provider="Gemini",
                model="gemini-3.5-flash"
            )

            attempts_list = []
            raw_result = None

            for attempt_number in range(1, 3):

                attempt = Attempt(
                    attempt_id=uuid.uuid4().int,
                    execution_id=execution.execution_id,
                    attempt_number=attempt_number,
                    started_at=datetime.now(timezone.utc)
                )

                start_time = time.perf_counter()

                try:
                    adapter_response = gemini_adapter.execute(prompt)

                except errors.ClientError as e:
                    attempt.status = StatusEnum.CLIENT_ERROR
                    print("Prompt", prompt.prompt_id, "failed:", e)

                except errors.ServerError as e:
                    attempt.status = StatusEnum.SERVER_ERROR
                    print("Prompt", prompt.prompt_id, "failed:", e)

                except TimeoutError as e:
                    attempt.status = StatusEnum.TIMEOUT
                    print("Prompt", prompt.prompt_id, "failed:", e)

                except errors.APIError as e:
                    attempt.status = StatusEnum.CLIENT_ERROR
                    print("Prompt", prompt.prompt_id, "failed:", e)

                else:
                    attempt.status = StatusEnum.SUCCESS
                    attempt.input_tokens = adapter_response.input_tokens
                    attempt.output_tokens = adapter_response.output_tokens
                    attempt.total_tokens = adapter_response.total_tokens

                    raw_result = response_handler_instance.handle_response(
                        adapter_response,
                        attempt.attempt_id,
                        sequence_number
                    )

                finally:
                    attempt.response_code = None
                    attempt.finished_at = datetime.now(timezone.utc)
                    attempt.latency = time.perf_counter() - start_time
                    attempts_list.append(attempt)

                if attempt.status == StatusEnum.SUCCESS:
                    break

            list_of_tuples.append(
                (execution, attempts_list, raw_result)
            )

        return list_of_tuples
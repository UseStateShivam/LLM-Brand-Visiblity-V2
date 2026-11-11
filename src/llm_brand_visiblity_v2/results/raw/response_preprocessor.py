from llm_brand_visiblity_v2.schemas import Attempt
from llm_brand_visiblity_v2.schemas import PromptExec
from llm_brand_visiblity_v2.schemas import RawResult
from llm_brand_visiblity_v2.schemas import Prompt

class ResponsePreprocessor:
    def combine_prompt_with_response(self, execution_output: list[tuple[PromptExec, list[Attempt], RawResult | None]], prompts: list[Prompt]) -> tuple[list[tuple[Prompt, RawResult]], list[Prompt]]:
        prompt_id_to_raw_result: dict[int, RawResult] = {}
        prompt_result_pair_list: list[tuple[Prompt, RawResult]] = []

        prompts_without_successful_response = []

        for execution, _, raw_result in execution_output:
            if raw_result is None:
                continue
            prompt_id_to_raw_result[execution.prompt_id] = raw_result

        for prompt in prompts:
            if prompt.prompt_id in prompt_id_to_raw_result:
                prompt_result_pair_list.append((prompt, prompt_id_to_raw_result[prompt.prompt_id]))
            else:
                print(f"No successful response found for prompt: {prompt.prompt_id}")
                prompts_without_successful_response.append(prompt)

        return prompt_result_pair_list, prompts_without_successful_response
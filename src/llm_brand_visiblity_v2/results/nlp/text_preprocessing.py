
import re
import unicodedata

from llm_brand_visiblity_v2.schemas import NormalizedPromptResponse
from llm_brand_visiblity_v2.schemas import RawResult
from llm_brand_visiblity_v2.schemas import Prompt


class PreprocessText:

    def normalize_response_text(
        self,
        input_pairs: list[tuple[Prompt, RawResult]]
    ) -> list[NormalizedPromptResponse]:

        normalized_pairs: list[NormalizedPromptResponse] = []

        for prompt, raw_response in input_pairs:

            raw_response_content = raw_response.content

            # Unicode normalization
            unicode_normalized_content = unicodedata.normalize(
                "NFC",
                raw_response_content
            )

            # Whitespace normalization
            normalized_line_endings = (
                unicode_normalized_content
                .replace("\r\n", "\n")
                .replace("\r", "\n")
            )

            lines = normalized_line_endings.split("\n")

            normalized_lines = []
            inside_code_block = False
            code_fence = None

            for line in lines:

                stripped_line = line.lstrip()

                # Detect Markdown code fences
                fence_match = re.match(r"(```+|~~~+)", stripped_line)

                if fence_match:
                    current_fence = fence_match.group(1)[0]

                    if not inside_code_block:
                        inside_code_block = True
                        code_fence = current_fence

                    elif current_fence == code_fence:
                        inside_code_block = False
                        code_fence = None

                    normalized_lines.append(line)
                    continue

                # Preserve code block content
                if inside_code_block:
                    normalized_lines.append(line)
                    continue

                # Normalize whitespace in ordinary text
                leading_whitespace = re.match(r"^\s*", line).group()
                remaining_text = line[len(leading_whitespace):]

                normalized_text = re.sub(
                    r"\s+",
                    " ",
                    remaining_text
                ).rstrip()

                normalized_lines.append(
                    leading_whitespace + normalized_text
                )

            normalized_horizontal_spaces = "\n".join(normalized_lines)

            # Limit consecutive blank lines
            normalized_newlines = re.sub(
                r"\n{3,}",
                "\n\n",
                normalized_horizontal_spaces
            )

            whitespace_normalized = normalized_newlines.strip()

            normalized_pairs.append(
                NormalizedPromptResponse(
                    response_id=len(normalized_pairs) + 1,
                    prompt=prompt,
                    response=whitespace_normalized
                )
            )

        return normalized_pairs
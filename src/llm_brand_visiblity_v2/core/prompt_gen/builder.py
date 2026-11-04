from llm_brand_visiblity_v2.schemas import IntentEnum
from llm_brand_visiblity_v2.schemas import TypeEnum
from llm_brand_visiblity_v2.schemas import ContextEnum
from llm_brand_visiblity_v2.schemas import Prompt
from llm_brand_visiblity_v2.schemas import BrandInput
from llm_brand_visiblity_v2.core.prompt_gen.seeder import templates

class BuildPrompts:
    def __init__(self, brand_input: BrandInput):
        self.brand_input = brand_input    
        self.prompt_list: list[Prompt] = []

    def build_prompt_list(self):
        if len(self.prompt_list) != 0:
            raise RuntimeError("Prompt list is already populated")

        self.available_contexts = []
        self.available_contexts.append(ContextEnum.BRANDLEVEL)

        if self.brand_input.products:
            self.available_contexts.append(ContextEnum.PRODUCTLEVEL)

        if self.brand_input.services:
            self.available_contexts.append(ContextEnum.SERVICELEVEL)

        self.available_types = []
        self.available_types.append(TypeEnum.BRANDED)
        self.available_types.append(TypeEnum.UNBRANDED)

        if self.brand_input.competitors:
            self.available_types.append(TypeEnum.COMPETITOR)

        for prompt_type in self.available_types:
            for intent in IntentEnum:
                for context in self.available_contexts:
                    if prompt_type == TypeEnum.UNBRANDED and context == ContextEnum.BRANDLEVEL:
                        continue
                    for template in templates[prompt_type][intent][context]:
                        if context == ContextEnum.BRANDLEVEL and prompt_type != TypeEnum.COMPETITOR:
                            formated_template = str.format(template, brand = self.brand_input.brand_name)

                            prompt = Prompt(
                                prompt_id = len(self.prompt_list) + 1,
                                prompt_type = prompt_type,
                                content = formated_template,
                                context = context,
                                intent = intent,
                            )
                            self.prompt_list.append(prompt)

                        elif context == ContextEnum.PRODUCTLEVEL and prompt_type != TypeEnum.COMPETITOR:
                            for product in self.brand_input.products:
                                formated_template = str.format(template, brand = self.brand_input.brand_name, product = product) 

                                prompt = Prompt(
                                    prompt_id = len(self.prompt_list) + 1,
                                    prompt_type = prompt_type,
                                    content = formated_template,
                                    context = context,
                                    intent = intent,
                                )
                                self.prompt_list.append(prompt)

                        elif context == ContextEnum.SERVICELEVEL and prompt_type != TypeEnum.COMPETITOR:
                            for service in self.brand_input.services:
                                formated_template = str.format(template, brand = self.brand_input.brand_name, service = service) 

                                prompt = Prompt(
                                    prompt_id = len(self.prompt_list) + 1,
                                    prompt_type = prompt_type,
                                    content = formated_template,
                                    context = context,
                                    intent = intent,
                                )
                                self.prompt_list.append(prompt)

                        elif prompt_type == TypeEnum.COMPETITOR and context == ContextEnum.PRODUCTLEVEL:
                            for competitor in self.brand_input.competitors:
                                for product in self.brand_input.products:
                                    formated_template = str.format(template, brand = self.brand_input.brand_name, competitor = competitor, product = product) 

                                    prompt = Prompt(
                                        prompt_id = len(self.prompt_list) + 1,
                                        prompt_type = prompt_type,
                                        content = formated_template,
                                        context = context,
                                        intent = intent,
                                    )
                                    self.prompt_list.append(prompt)

                        elif context == ContextEnum.BRANDLEVEL and prompt_type == TypeEnum.COMPETITOR:
                            for competitor in self.brand_input.competitors:
                                formated_template = str.format(template, brand = self.brand_input.brand_name, competitor = competitor)

                                prompt = Prompt(
                                    prompt_id = len(self.prompt_list) + 1,
                                    prompt_type = prompt_type,
                                    content = formated_template,
                                    context = context,
                                    intent = intent,
                                )
                                self.prompt_list.append(prompt)

                        elif context == ContextEnum.SERVICELEVEL and prompt_type == TypeEnum.COMPETITOR:
                            for competitor in self.brand_input.competitors:
                                for service in self.brand_input.services:
                                    formated_template = str.format(template, brand = self.brand_input.brand_name, service = service, competitor = competitor) 

                                    prompt = Prompt(
                                        prompt_id = len(self.prompt_list) + 1,
                                        prompt_type = prompt_type,
                                        content = formated_template,
                                        context = context,
                                        intent = intent,
                                    )
                                    self.prompt_list.append(prompt)

        return self.prompt_list
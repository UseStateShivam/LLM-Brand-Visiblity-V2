from abc import ABC
from abc import abstractmethod
from llm_brand_visiblity_v2.schemas import Prompt
from llm_brand_visiblity_v2.schemas import AdapterResponse

class BaseAdapter(ABC):
    @abstractmethod
    def execute(self, prompt: Prompt) -> AdapterResponse:
        pass
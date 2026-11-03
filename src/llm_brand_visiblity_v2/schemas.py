from pydantic import field_validator
from enum import Enum
from datetime import datetime
from pydantic import HttpUrl, ConfigDict, BaseModel

class TypeEnum(Enum):
    BRANDED = "branded"
    UNBRANDED = "unbranded"
    COMPETITOR = "competitor"

class IntentEnum(Enum):
    BUYING = "buying"
    INFORMATIONAL = "informational"
    COMPARISON = "comparison"

class StatusEnum(Enum):
    SUCCESS = "success"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    CLIENT_ERROR = "client_error"

class Prompt(BaseModel):
    model_config = ConfigDict(strict=True)

    prompt_id: int
    prompt_type: TypeEnum
    content: str
    category: str
    intent: IntentEnum  

class PromptExec(BaseModel):
    model_config = ConfigDict(strict=True)

    prompt_id: int
    execution_id: int
    provider: str
    model: str
    
class Attempt(BaseModel):
    model_config = ConfigDict(strict=True)

    attempt_id: int
    execution_id: int
    attempt_number: int
    status: StatusEnum
    response_code: int | None = None
    started_at: datetime
    finished_at: datetime | None = None

class RawResult(BaseModel):
    model_config = ConfigDict(strict=True)

    result_id: int
    attempt_id: int
    content: str
    sequence_number: int

class BrandInput(BaseModel):
    model_config = ConfigDict(strict=True)
    
    brand_name: str
    website: HttpUrl
    competitors: list[str] | None = None
    products: list[str] | None = None
    services: list[str] | None = None
    niche: str

    @field_validator("brand_name", "niche", mode="before")
    @classmethod
    def str_validation(cls, x):
        x = x.strip()
        if len(x) == 0:
            raise ValueError("Field name can not be empty")
        return x
    
    @field_validator("competitors", "products", "services", mode="before")
    @classmethod
    def list_validation(cls, x):
        clean_list = []

        if x is None:
            return None

        if len(x) == 0:
            raise ValueError("List can not be empty")

        for i in range(len(x)):
            c = x[i].strip()
            if len(c) == 0:
                raise ValueError("List item can not be empty")
            if len(c) > 350:
                raise ValueError("List item too long")
            clean_list.append(c)

        return clean_list
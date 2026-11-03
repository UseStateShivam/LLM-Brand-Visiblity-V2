from datetime import datetime
from enum import Enum
from pydantic import ConfigDict
from pydantic import BaseModel

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
    response_code: int | None
    started_at: datetime
    finished_at: datetime | None

class RawResult(BaseModel):
    model_config = ConfigDict(strict=True)

    result_id: int
    attempt_id: int
    content: str
    sequence_number: int
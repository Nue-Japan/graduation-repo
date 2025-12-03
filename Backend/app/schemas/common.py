from pydantic import BaseModel
from typing import Optional, Any

class APIResponse(BaseModel):
    status: str              # "success" or "error"
    message: str             # Description of the response
    data: Optional[Any] = None  # Optional data payload

    class Config:
        from_attributes = True
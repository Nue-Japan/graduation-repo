from pydantic import BaseModel
from datetime import datetime

# Pydantic models for user creation and response
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "general"

# Response model for user data
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
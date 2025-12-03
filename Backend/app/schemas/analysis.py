from pydantic import BaseModel
from typing import List, Optional

# Pydantic models for analysis request and response
class AnalysisRequest(BaseModel):
    context: str
    data_text: str
    model_name: Optional[str] = "gemini-2.5-flash"

# Response model for analysis results
class AnalysisResponse(BaseModel):
    advice: str
    key_points: List[str]   
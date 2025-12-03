from fastapi import APIRouter
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.ai_service import generate_insight

# API router for analysis endpoints
router = APIRouter()

# Endpoint to analyze data and generate insights
@router.post("/",response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    """
    Unity endpoint to analyze data and generate insights using AI models.
    """
    result = await generate_insight(
        context=request.context,
        data_text=request.data_text,
        model_name=request.model_name,
    )
    return result
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine,Base
from app.api import analysis

from app.api import analysis
from app.api import users

from app.models import user as user_model

from app.schemas.analysis import AnalysisResponse, DataPoint

from app.services.ai_analysis import analyze_text_with_gemini

from app.api import health

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Data-platform-backend-veta",version="1.0.0")

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://ar-dataplatform-veta.com",
    "*"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディの定義（Unityから送られてくるデータの形）
class AnalysisRequest(BaseModel):
    raw_text: str # 生データ
    


# Include API routers
app.include_router(analysis.router, prefix="/api/analysis", tags=["AI_analysis"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(health.router, prefix="/api/system", tags=["health"])

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "backend is running with Gemini AI!"}

# @app.get("/api/analysis/mock", response_model=AnalysisResponse)
# async def get_mock_analysis():
#     """
#     3Dグラフ描画用 兼 AIアドバイスのダミーデータを返す
#     """
#     return AnalysisResponse(
#         title="2025年度 顧客満足度分析",
#         summary="若年層の支持が急増しています。",
#         advice="20代向けのキャンペーンを強化すべきです。",
#         key_points=["20代: +40%", "50代: 横ばい"],
        
#         recommended_graph_type="scatter", 

#         data_points=[
#             DataPoint(label="10代", value=5.0),
#             DataPoint(label="20代", value=25.0),
#             DataPoint(label="30代", value=15.0),
#             DataPoint(label="40代", value=10.0),
#             DataPoint(label="50代", value=8.0),
#         ]
#     )
#     pass
    
@app.get("/api/system/health")
def health_check():
    return {"status": "success", "message": "System is healthy"}

@app.post("/api/analysis/generate", response_model=AnalysisResponse)
async def generate_analysis(request: AnalysisRequest):
    """
    Unityから送られたテキストをGeminiで分析し、結果を返す
    """
    print(f"Received text: {request.raw_text}") # ログ確認用
    
    if not request.raw_text:
        raise HTTPException(status_code=400, detail="Text input is empty")

    # AIサービスを呼び出す
    response = await analyze_text_with_gemini(request.raw_text)
    return response
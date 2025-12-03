from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine,Base
from app.api import analysis

from app.api import analysis
from app.api import users

from app.models import user as user_model

from app.schemas.analysis import AnalysisResponse, DataPoint

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

# Include API routers
app.include_router(analysis.router, prefix="/api/analysis", tags=["AI_analysis"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(health.router, prefix="/api/system", tags=["health"])

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "backend is running with Gemini AI!"}

@app.get("/api/analysis/mock", response_model=AnalysisResponse)
async def get_mock_analysis():
    """
    3Dグラフ描画用 兼 AIアドバイスのダミーデータを返す
    """
    return AnalysisResponse(
        title="2025年度 顧客満足度分析",
        summary="若年層の支持が急増しています。",
        advice="20代向けのキャンペーンを強化すべきです。",
        key_points=["20代: +40%", "50代: 横ばい"],
        
        recommended_graph_type="scatter", 

        data_points=[
            DataPoint(label="10代", value=5.0),
            DataPoint(label="20代", value=25.0),
            DataPoint(label="30代", value=15.0),
            DataPoint(label="40代", value=10.0),
            DataPoint(label="50代", value=8.0),
        ]
    )
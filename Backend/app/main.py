from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine,Base
from app.api import analysis

from app.api import analysis
from app.api import users

from app.models import user as user_model

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

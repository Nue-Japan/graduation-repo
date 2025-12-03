from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.common import APIResponse

router = APIRouter()

@router.get("/health", response_model=APIResponse)
def health_check(db: Session = Depends(get_db)):
    """
    サーバーとデータベースの生存確認
    """
    try:
        # DBに軽いクエリ(SELECT 1)を投げて接続テスト
        db.execute(text("SELECT 1"))
        return APIResponse(
            status="success",
            message="System is healthy",
            data={"database": "connected", "api": "running"}
        )
    except Exception as e:
        return APIResponse(
            status="error",
            message="Database connection failed",
            data={"error": str(e)}
        )
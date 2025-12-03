from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.common import APIResponse

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=APIResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # ユーザー名の重複チェック
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # ハッシュ化して保存
    hashed_pw = pwd_context.hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw, role=user.role)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return APIResponse(status="success", message="User created", data=UserResponse.model_validate(new_user))

@router.get("/", response_model=APIResponse)
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return APIResponse(status="success", message="User list", data=[UserResponse.model_validate(u) for u in users])
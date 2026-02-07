from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.users import User
from app.schemas.users import UserResponse
from app.utils.auth import get_current_user

# ルーター作成
router = APIRouter(
    prefix="/users",
    tags=["ユーザー"]
)

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    自分のプロフィールを取得
    
    **認証が必要です**
    """
    return current_user

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    全ユーザーの一覧を取得
    
    **認証が必要です**
    """
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    指定したIDのユーザー情報を取得
    
    **認証が必要です**
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが見つかりません"
        )
    
    return user
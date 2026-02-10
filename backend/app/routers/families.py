from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import secrets

from app.database import get_db
from app.models.users import User
from app.models.family import Family
from app.schemas.family import FamilyCreate, FamilyResponse
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/families",
    tags=["家族グループ"]
)

@router.post("/", response_model=FamilyResponse, status_code=status.HTTP_201_CREATED)
def create_family(
    family: FamilyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    新しい家族グループを作成
    
    作成したユーザーが自動的にその家族に所属します
    """
    # 既に家族に所属している場合はエラー
    if current_user.family_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既に家族グループに所属しています"
        )
    
    # 招待コードを生成（8文字のランダム文字列）
    invite_code = secrets.token_urlsafe(6)
    
    # 家族グループを作成
    new_family = Family(
        name=family.name,
        invite_code=invite_code
    )
    db.add(new_family)
    db.commit()
    db.refresh(new_family)
    
    # 作成者をその家族に追加
    current_user.family_id = new_family.id
    db.commit()
    db.refresh(new_family)
    
    return new_family

@router.get("/me", response_model=FamilyResponse)
def get_my_family(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    自分が所属している家族グループの情報を取得
    """
    if current_user.family_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家族グループに所属していません"
        )
    
    family = db.query(Family).filter(Family.id == current_user.family_id).first()
    
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="家族グループが見つかりません"
        )
    
    return family

@router.post("/join/{invite_code}", response_model=FamilyResponse)
def join_family_by_invite_code(
    invite_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    招待コードで家族グループに参加
    """
    # 既に家族に所属している場合はエラー
    if current_user.family_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既に家族グループに所属しています"
        )
    
    # 招待コードで家族を検索
    family = db.query(Family).filter(Family.invite_code == invite_code).first()
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="招待コードが無効です"
        )
    
    # 家族に参加
    current_user.family_id = family.id
    db.commit()
    db.refresh(family)
    
    return family

@router.post("/{family_id}/members", response_model=FamilyResponse)
def join_family(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    既存の家族グループに参加（メンバーとして追加）
    """
    # 既に家族に所属している場合はエラー
    if current_user.family_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="既に家族グループに所属しています"
        )
    
    # 家族グループの存在確認
    family = db.query(Family).filter(Family.id == family_id).first()
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された家族グループが見つかりません"
        )
    
    # 家族に参加
    current_user.family_id = family_id
    db.commit()
    db.refresh(family)
    
    return family

@router.delete("/{family_id}/members/me")
def leave_family(
    family_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    家族グループから離脱（自分をメンバーから削除）
    """
    if current_user.family_id != family_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="指定された家族グループに所属していません"
        )
    
    current_user.family_id = None
    db.commit()
    
    return {"message": "家族グループから離脱しました"}
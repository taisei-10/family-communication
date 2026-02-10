from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# 家族メンバーの簡易表示用
class FamilyMemberResponse(BaseModel):
    """
    家族メンバーの情報
    """
    id: int
    username: str
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# 家族作成時のリクエスト
class FamilyCreate(BaseModel):
    """
    家族グループ作成時のリクエストボディ
    """
    name: str

# 家族情報のレスポンス
class FamilyResponse(BaseModel):
    """
    家族グループ情報のレスポンス
    """
    id: int
    name: str
    invite_code: str
    created_at: datetime
    members: List[FamilyMemberResponse] = []
    
    class Config:
        from_attributes = True
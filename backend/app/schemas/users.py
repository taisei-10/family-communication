from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ユーザー登録時に受け取るデータ
class UserCreate(BaseModel):
    """
    ユーザー新規登録時のリクエストボディ
    """
    username: str
    email: Optional[EmailStr] = None
    password: str
    full_name: Optional[str] = None

# ユーザーログイン時に受け取るデータ
class UserLogin(BaseModel):
    """
    ユーザーログイン時のリクエストボディ
    """
    username: str
    password: str   

# APIで返すユーザー情報
class UserResponse(BaseModel):
    """
    ユーザー情報のレスポンスモデル
    """
    id: int
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# トークンのレスポンス
class Token(BaseModel):
    """
    ログイン成功時に返すトークン
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    トークンデータモデル
    """
    username: Optional[str] = None
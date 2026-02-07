from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.database import get_db
from app.models.users import User
from app.schemas.users import TokenData

load_dotenv()

# 環境変数から設定を読み込む
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2の設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 認証エラー用の例外（複数の関数で使用）
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="認証情報を確認できませんでした",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWTアクセストークンを生成
    
    Args:
        data: トークンに含めるデータ（ユーザー名など）
        expires_delta: トークンの有効期限
    
    Returns:
        str: JWTトークン
    """
    to_encode = data.copy()
    
    # 有効期限を設定
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # トークンを生成
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """
    JWTトークンを検証してデータを取り出す
    
    Args:
        token: 検証するJWTトークン
    
    Returns:
        TokenData: トークンから取り出したデータ
    """
    try:
        # トークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
        return token_data
    
    except JWTError:
        raise credentials_exception
    

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    現在ログインしているユーザーを取得
    （保護されたエンドポイントで使用）
    
    Args:
        token: リクエストヘッダーから取得したJWTトークン
        db: データベースセッション
    
    Returns:
        User: ログイン中のユーザー
    
    Raises:
        HTTPException: 認証失敗時
    """
    # トークンを検証
    token_data = verify_token(token)
    
    # データベースからユーザーを取得
    user = db.query(User).filter(User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    
    return user
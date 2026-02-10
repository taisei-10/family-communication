from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserResponse, Token
from app.utils.security import get_password_hash, verify_password
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# ルーター作成（/auth プレフィックス）
router = APIRouter(
    prefix="/auth",
    tags=["認証"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    新規ユーザー登録
    
    - **username**: ユーザー名（一意）
    - **email**: メールアドレス（一意）
    - **password**: パスワード
    - **full_name**: フルネーム（オプション）
    """
    # ユーザー名が既に存在するかチェック
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このユーザー名は既に使用されています"
        )
    
    # メールアドレスが提供されている場合のみ重複チェック
    if user.email:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="このメールアドレスは既に使用されています"
            )
    
    # パスワードをハッシュ化
    hashed_password = get_password_hash(user.password)
    
    # 新しいユーザーを作成
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    # データベースに保存
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 保存後のデータ（IDなど）を取得
    
    return new_user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    ログイン
    
    - **username**: ユーザー名
    - **password**: パスワード
    
    成功するとJWTトークンを返します
    """
    # ユーザーを取得
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # ユーザーが存在しない、またはパスワードが間違っている
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWTトークンを生成
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
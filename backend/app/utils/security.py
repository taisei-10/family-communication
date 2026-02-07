from passlib.context import CryptContext

# パスワードのハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    平文パスワードとハッシュ化されたパスワードを比較して検証する
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化する
    """
    return pwd_context.hash(password)

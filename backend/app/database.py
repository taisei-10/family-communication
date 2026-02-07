from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベースのURL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./family_communication.db")

# SQLAlchemyの設定
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
    )

# データベースセッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベースセッションを取得するための依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """
    ユーザーモデル
    家族メンバーの情報を保存
    """
    __tablename__ = "users"

    # カラム定義
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)

    # 家族への紐付け
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)

    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # リレーション: 所属する家族
    family = relationship("Family", back_populates="members")
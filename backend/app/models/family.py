from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Family(Base):
    """
    家族グループモデル
    複数のユーザーが1つの家族に所属する
    """
    __tablename__ = "families"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # 家族名
    
    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーション: この家族に所属するメンバー
    members = relationship("User", back_populates="family")
    schedules = relationship("Schedule", back_populates="family")
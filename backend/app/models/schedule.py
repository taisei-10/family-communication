from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Schedule(Base):
    """
    スケジュールモデル
    帰宅予定、食事の有無、車の予約、その他の予定を統合管理
    """
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)
    
    # スケジュールの種類: "return"(帰宅), "meal"(食事), "car"(車), "event"(その他)
    schedule_type = Column(String, nullable=False, index=True)
    
    # 基本情報
    title = Column(String, nullable=True)  
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=True)  # 帰宅時間や車の開始時間など
    end_time = Column(Time, nullable=True)    # 車の終了時間など
    
    # 食事フラグ（schedule_type="meal" の時のみ使用）
    breakfast = Column(Boolean, nullable=True)
    lunch = Column(Boolean, nullable=True)
    dinner = Column(Boolean, nullable=True)
    
    # 車情報（schedule_type="car" の時のみ使用）
    car_name = Column(String, nullable=True)
    
    # タイムスタンプ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーション
    user = relationship("User", back_populates="schedules")
    family = relationship("Family", back_populates="schedules")
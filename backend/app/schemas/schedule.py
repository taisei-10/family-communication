from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional

# スケジュール作成（全タイプ統合）
class ScheduleCreate(BaseModel):
    """
    スケジュール作成リクエスト
    """
    schedule_type: str = Field(..., description="return, meal, car, event のいずれか")
    title: Optional[str] = None
    description: Optional[str] = None
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    # 食事用（schedule_type="meal" の時のみ使用）
    breakfast: Optional[bool] = None
    lunch: Optional[bool] = None
    dinner: Optional[bool] = None
    
    # 車用（schedule_type="car" の時のみ使用）
    car_name: Optional[str] = None 

# ユーザー情報（簡易版）
class ScheduleUserResponse(BaseModel):
    """
    スケジュールに含まれるユーザー情報
    """
    id: int
    username: str
    full_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# スケジュールのレスポンス
class ScheduleResponse(BaseModel):
    """
    スケジュール情報のレスポンス
    """
    id: int
    user_id: int
    family_id: int
    schedule_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    
    # 食事情報
    breakfast: Optional[bool] = None
    lunch: Optional[bool] = None
    dinner: Optional[bool] = None
    
    # 車情報
    car_name: Optional[str] = None
    
    # ユーザー情報
    user: ScheduleUserResponse
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
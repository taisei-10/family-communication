from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.models.users import User
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleResponse
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/schedules",
    tags=["スケジュール"]
)

@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    新しいスケジュールを作成
    
    - **return**: 帰宅予定（start_time必須）
    - **meal**: 食事の有無（breakfast, lunch, dinner）
    - **car**: 車の予約（car_name, start_time, end_time必須）
    - **event**: その他のイベント（title必須）
    """
    # 家族に所属していない場合はエラー
    if current_user.family_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="家族グループに所属していません"
        )
    
    # バリデーション
    if schedule.schedule_type == "event" and not schedule.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="イベントタイプの場合、タイトルは必須です"
        )
    
    if schedule.schedule_type == "car" and (not schedule.car_name or not schedule.start_time or not schedule.end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="車予約の場合、車の名前、開始時刻、終了時刻は必須です"
        )
    
    # 新しいスケジュールを作成
    new_schedule = Schedule(
        user_id=current_user.id,
        family_id=current_user.family_id,
        **schedule.model_dump()
    )
    
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    
    return new_schedule

@router.get("/", response_model=List[ScheduleResponse])
def get_schedules(
    schedule_type: str = None,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    家族全員のスケジュールを取得
    
    - **schedule_type**: フィルター（return, meal, car, event）
    - **start_date**: 開始日
    - **end_date**: 終了日
    """
    if current_user.family_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="家族グループに所属していません"
        )
    
    query = db.query(Schedule).filter(Schedule.family_id == current_user.family_id)
    
    # フィルター適用
    if schedule_type:
        query = query.filter(Schedule.schedule_type == schedule_type)
    
    if start_date:
        query = query.filter(Schedule.date >= start_date)
    
    if end_date:
        query = query.filter(Schedule.date <= end_date)
    
    schedules = query.order_by(Schedule.date, Schedule.start_time).all()
    
    return schedules

@router.get("/me", response_model=List[ScheduleResponse])
def get_my_schedules(
    schedule_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    自分のスケジュールのみを取得
    """
    query = db.query(Schedule).filter(Schedule.user_id == current_user.id)
    
    if schedule_type:
        query = query.filter(Schedule.schedule_type == schedule_type)
    
    schedules = query.order_by(Schedule.date, Schedule.start_time).all()
    
    return schedules

@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    特定のスケジュールを取得
    """
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="スケジュールが見つかりません"
        )
    
    # 自分の家族のスケジュールかチェック
    if schedule.family_id != current_user.family_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="このスケジュールにアクセスする権限がありません"
        )
    
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    スケジュールを更新（自分が作成したスケジュールのみ）
    """
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="スケジュールが見つかりません"
        )
    
    # 作成者本人かチェック
    if schedule.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="自分のスケジュールのみ更新できます"
        )
    
    # 更新
    for key, value in schedule_update.model_dump().items():
        setattr(schedule, key, value)
    
    db.commit()
    db.refresh(schedule)
    
    return schedule

@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    スケジュールを削除（自分が作成したスケジュールのみ）
    """
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="スケジュールが見つかりません"
        )
    
    # 作成者本人かチェック
    if schedule.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="自分のスケジュールのみ削除できます"
        )
    
    db.delete(schedule)
    db.commit()
    
    return {"message": "スケジュールを削除しました"}
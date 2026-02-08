from fastapi import FastAPI
from app.database import engine, Base
from app.models import users, family, schedule
from app.routers import auth, users, families, schedules

# データベースのテーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI(
    title="Family Communication API",
    description="家族向けコミュニケーションアプリのAPI",
    version="1.0.0"   
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(families.router)
app.include_router(schedules.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Family Communication API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
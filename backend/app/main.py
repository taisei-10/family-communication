from fastapi import FastAPI
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Viteのデフォルトポート
        "http://127.0.0.1:5173",      # 127.0.0.1版も追加
    ],
    allow_credentials=True,
    allow_methods=["*"],              # すべてのHTTPメソッドを許可（OPTIONS含む）
    allow_headers=["*"],              # すべてのヘッダーを許可
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
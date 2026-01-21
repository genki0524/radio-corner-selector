"""
FastAPI メインアプリケーション
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db, SessionLocal
from routers import memos, profiles, personalities, programs, corners, mails, analyze, recommendations
from models import User

# FastAPIアプリケーション
app = FastAPI(
    title=settings.app_name,
    description="ラジオ投稿管理API - メモからコーナーへの自動振り分け",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(memos.router, prefix="/api")
app.include_router(profiles.router, prefix="/api")
app.include_router(personalities.router, prefix="/api")
app.include_router(programs.router, prefix="/api")
app.include_router(corners.router, prefix="/api")
app.include_router(mails.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(recommendations.router)


@app.on_event("startup")
async def startup_event():    
    # 開発環境: データが存在しない場合はシードデータを投入
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            print("📊 データベースが空です。シードデータを投入します...")
            from seed_data import seed_data
            seed_data()
    finally:
        db.close()


@app.get("/")
def read_root():
    """ルートエンドポイント"""
    return {
        "message": "Radio Corner Selector API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}

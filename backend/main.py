"""
FastAPI メインアプリケーション
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from routers import memos, profiles, personalities, programs, corners, mails, analyze

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


@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    init_db()


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

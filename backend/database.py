"""
データベース接続設定
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

# SQLAlchemyエンジン作成
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # 接続の健全性チェック
    pool_size=5,  # コネクションプールサイズ
    max_overflow=10,  # 最大追加接続数
)

# セッションファクトリ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラス
Base = declarative_base()


def get_db():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """データベースを初期化"""
    Base.metadata.create_all(bind=engine)

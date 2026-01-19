"""
データベース接続設定
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

# SQLAlchemyエンジン作成
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite用
    echo=settings.debug,
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

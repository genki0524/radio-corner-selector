"""
環境変数と設定管理
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # データベース
    database_url: str = "sqlite:///./radio_corner_selector.db"
    
    # Google Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-pro"
    
    # アプリケーション
    app_name: str = "Radio Corner Selector API"
    debug: bool = True
    
    # CORS
    cors_origins: list[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

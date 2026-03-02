"""
環境変数と設定管理
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Union

class Settings(BaseSettings):
    """アプリケーション設定"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    # データベース
    database_url: str = "postgresql://radio_user:radio_password@db:5432/radio_corner_selector"
    
    # Google Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_temperature: float = 0.7

    # OpenAI API
    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = Field(default=1536, le=1536)
    
    # アプリケーション
    app_name: str = "Radio Corner Selector API"
    debug: bool = True
    
    # CORS (環境変数からはカンマ区切り文字列またはリストとして受け取る)
    cors_origins: Union[str, list[str]] = ["http://localhost:8501", "http://localhost:3000"]
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """環境変数からカンマ区切りの文字列をリストに変換"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v


settings = Settings(embedding_dimension=1024)

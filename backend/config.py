"""
環境変数と設定管理
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Union

class Settings(BaseSettings):
    """アプリケーション設定"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    # データベース
    database_url: str = "postgresql://radio_user:radio_password@localhost:5432/radio_corner_selector"
    
    # Google Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-pro"
    
    # LangChain & LLM Settings
    # HuggingFace Embedding Model
    embedding_model_name: str = "intfloat/multilingual-e5-large"
    embedding_dimension: int = 1024
    
    # Ollama LLM Settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:latest"
    ollama_temperature: float = 0.7
    
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


settings = Settings()

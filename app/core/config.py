from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    log_dir: str = 'logs'

    openrouter_api_key: str
    openrouter_base_url: str = 'https://openrouter.ai/api/v1/chat/completions'
    openrouter_model: str = 'google/gemini-2.0-flash-001'
    openrouter_temperature: float = 0.0
    llm_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = Settings()

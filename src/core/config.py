from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Настройки приложения, загружаемые из .env файла"""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    """Кэшируемая функция для получения настроек"""
    return Settings()

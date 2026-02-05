"""LifeHub Configuration"""
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    app_name: str = "LifeHub"
    app_env: str = "development"
    debug: bool = True
    app_access_token: str = "change-me-in-production"
    
    # Database
    database_url: str = "postgresql://localhost:5432/lifehub"
    
    # OpenAI
    openai_api_key: str = ""
    
    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    # Weather
    weather_api_key: str = ""
    default_city: str = "Warsaw"
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Timezone
    timezone: str = "Europe/Warsaw"
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins list."""
        origins = [self.frontend_url]
        if self.app_env == "development":
            origins.extend([
                "http://localhost:3000",
                "http://127.0.0.1:3000",
            ])
        return origins
    
    @property
    def database_url_sync(self) -> str:
        """Get sync database URL for Alembic migrations."""
        return self.database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()

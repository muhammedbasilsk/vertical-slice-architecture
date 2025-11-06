"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "sqlite:///./app.db"
    api_version: str = "v1"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

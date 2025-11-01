"""Configuration module for the application."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Database
    database_url: str

    # API Keys
    anthropic_api_key: str
    openai_api_key: str

    # Security
    secret_key: str
    algorithm: str = "HS256"

    # Environment
    debug: bool = False
    environment: str = "development"

    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


settings = get_settings()

"""Application settings module.

This module defines the application settings.
It uses Pydantic's BaseSettings to load environment variables
and provides a structured way to access configuration values.
"""

from enum import Enum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(str, Enum):
    """Enumeration for application environments.

    Defines the environment in which the application is running.
    """

    development = "development"
    production = "production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    environment: Env = Env.development
    app_name: str = "Baynext API"
    bucket_name: str = "lgrosjean-blob"
    ml_api_secret_api_key: SecretStr
    database_url: SecretStr
    blob_read_write_token: SecretStr
    auth_secret: SecretStr

    model_config = SettingsConfigDict(env_file=".env")

    def is_prod(self) -> bool:
        """Check if the application is running in production environment."""
        return self.environment == Env.production


settings = Settings()

"""Application settings module.

This module defines the application settings.
It uses Pydantic's BaseSettings to load environment variables
and provides a structured way to access configuration values.
"""

import tomllib
from enum import Enum
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Read version from pyproject.toml
with Path.open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)
    version = pyproject["project"]["version"]

DESCRIPTION = """
This is the API documentation for the Baynext project management system.
It provides endpoints for managing projects, datasets, pipelines, and more.

Authentication is handled via JWT tokens, and the system supports
role-based access control to ensure secure and efficient project management.
"""


class Env(str, Enum):
    """Enumeration for application environments.

    Defines the environment in which the application is running.
    """

    development = "development"
    production = "production"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    APP_NAME: str = "Baynext API"
    VERSION: str = version
    DEBUG: bool = True
    DESCRIPTION: str = DESCRIPTION

    # Security
    AUTH_SECRET: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY_HEADER: str = "x-baynext-api-key"
    """Header name for API key authentication."""
    API_KEY_QUERY: str = "key"
    """Query parameter name for API key authentication."""

    # CORS - includes Vercel domains
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://baynext.tech",  # Your production domain
    ]

    environment: Env = Env.development

    bucket_name: str = "lgrosjean-blob"
    ml_api_secret_api_key: SecretStr
    database_url: SecretStr
    blob_read_write_token: SecretStr
    auth_secret: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        use_enum_values=True,
    )

    def is_prod(self) -> bool:
        """Check if the application is running in production environment."""
        return self.environment == Env.production


settings = Settings()

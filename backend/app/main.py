"""FastAPI application main module.

This module initializes the FastAPI application with middleware,
security configurations, and API routers.
"""

import tomllib
from pathlib import Path

from fastapi import FastAPI

from .api.v1 import router as v1_router
from .core.middleware import add_middleware
from .core.settings import settings

LONG_DESCRIPTION = """
This is the API documentation for the Baynext project management system.
It provides endpoints for managing projects, datasets, pipelines, and more.

Authentication is handled via JWT tokens, and the system supports
role-based access control to ensure secure and efficient project management.
"""

# Read version from pyproject.toml
with Path.open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)
    version = pyproject["project"]["version"]

app = FastAPI(
    title=settings.app_name,
    redoc_url=None,
    description=LONG_DESCRIPTION,
    version=version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Add middleware (centralized configuration)
add_middleware(app)

# Include routers after middleware
app.include_router(v1_router)

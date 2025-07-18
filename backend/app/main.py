"""FastAPI application main module.

This module initializes the FastAPI application with middleware,
security configurations, and API routers.
"""

import os

from fastapi import FastAPI

from .api.v1 import router as v1_router
from .core.middleware import add_middleware
from .core.settings import settings

app = FastAPI(
    title=settings.app_name,
    redoc_url=None,
    docs_url="/docs" if not os.getenv("RENDER") else None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Add middleware (centralized configuration)
add_middleware(app)

# Include routers after middleware
app.include_router(v1_router)

"""FastAPI application main module.

This module initializes the FastAPI application with middleware,
security configurations, and API routers.
"""

from fastapi import FastAPI

from .core.middleware import add_middleware
from .core.settings import settings
from .routers.v1 import router as v1_router

app = FastAPI(
    title=settings.APP_NAME,
    redoc_url=None,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Add middleware (centralized configuration)
add_middleware(app)

# Include routers after middleware
app.include_router(v1_router)

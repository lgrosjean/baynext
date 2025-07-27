"""API v1 module for project management."""

import importlib

from .base import router

# Dynamically import the project_id router
project_id_router = importlib.import_module(
    "app.routers.v1.projects.[project_id]",
).router


router.include_router(project_id_router)

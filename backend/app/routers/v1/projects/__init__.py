"""API v1 module for project management."""

import importlib

from fastapi import APIRouter

from .base import router as base_router

# Dynamically import the project_id router
project_id_router = importlib.import_module(
    "app.routers.v1.projects.[project_id]",
).router

router = APIRouter(prefix="/projects")
# Include the base router for project management
router.include_router(base_router)
# Include the project_id router for specific project operations
router.include_router(project_id_router)

for route in router.routes:
    route.path = route.path.rstrip("/")

"""API router for dataset-related endpoints."""

import importlib

from fastapi import APIRouter

from .base import router as base_router

# Dynamically import the dataset_id router
dataset_id_router = importlib.import_module(
    "app.routers.v1.projects.[project_id].datasets.[dataset_id]",
).router

router = APIRouter(prefix="/datasets")
# Include the base router for dataset management
router.include_router(base_router)
# Include the dataset_id router for specific dataset operations
router.include_router(dataset_id_router)

for route in router.routes:
    route.path = route.path.rstrip("/")

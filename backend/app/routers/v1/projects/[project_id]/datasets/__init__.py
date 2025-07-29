"""API router for dataset-related endpoints."""

import importlib

from .base import router

# Dynamically import the dataset_id router
dataset_id_router = importlib.import_module(
    "app.routers.v1.projects.[project_id].datasets.[dataset_id]",
).router

router.include_router(dataset_id_router)

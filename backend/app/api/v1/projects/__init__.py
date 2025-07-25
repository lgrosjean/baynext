"""API v1 module for project management."""

import importlib

from fastapi import APIRouter

from .base import router as base_router
from app.core.dependencies import CheckAuthDeps

# Dynamically import the project_id router
project_id_router = importlib.import_module("app.api.v1.projects.[project_id]").router

router = APIRouter(
    prefix="/projects",
    dependencies=[CheckAuthDeps],
)

router.include_router(base_router)
router.include_router(project_id_router)

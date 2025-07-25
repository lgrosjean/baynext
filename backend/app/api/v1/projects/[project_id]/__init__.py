"""API router for project-related endpoints.

This module defines the API endpoints for managing resources related to a specific project.
"""

from fastapi import APIRouter

from .base import router as base_router
from .datasets import router as datasets_router
from .keys import router as keys_router
from .pipelines import router as pipelines_router

router = APIRouter(
    prefix="/{project_id}",
)

router.include_router(base_router)
router.include_router(datasets_router)
router.include_router(keys_router)
router.include_router(pipelines_router)

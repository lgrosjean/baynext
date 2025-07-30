"""API router for project-related endpoints.

This module defines the API endpoints for managing resources related to a specific project.
"""

from fastapi import APIRouter

from .base import router as base_router
from .datasets import router as datasets_router

router = APIRouter()
router.include_router(base_router)
router.include_router(datasets_router)

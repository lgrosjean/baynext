"""API router for specific dataset-related endpoints."""

from fastapi import APIRouter

from .base import router as base_router

router = APIRouter()
# Include the base router for dataset management
router.include_router(base_router)

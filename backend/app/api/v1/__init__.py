"""API v1 module."""

from fastapi import APIRouter

from app.api.v1 import auth, health, projects

router = APIRouter(prefix="/v1")

router.include_router(health.router)
router.include_router(projects.router)
router.include_router(auth.router)

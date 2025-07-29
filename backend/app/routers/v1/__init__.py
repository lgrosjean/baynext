"""API v1 module."""

from fastapi import APIRouter

from . import auth, me, projects

router = APIRouter(prefix="/v1")

router.include_router(projects.router)
router.include_router(auth.router)
router.include_router(me.router)

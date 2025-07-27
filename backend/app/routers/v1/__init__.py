"""API v1 module."""

from fastapi import APIRouter, Request

from . import auth, health, me, projects

router = APIRouter(prefix="/v1")

router.include_router(health.router)
router.include_router(projects.router)
router.include_router(auth.router)
router.include_router(me.router)


@router.get("/", include_in_schema=False)
async def root(request: Request) -> dict:
    """Root endpoint for API v1.

    Returns basic information about the API.
    """
    return {
        "message": request.app.title,
        "version": request.app.version,
        "authentication": "Bearer Token required",
    }

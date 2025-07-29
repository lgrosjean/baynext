"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
    include_in_schema=False,
)


@router.get("/")
async def health_check() -> dict:
    """Health check endpoint.

    Returns the health status of the service.
    """
    return {"status": "healthy"}

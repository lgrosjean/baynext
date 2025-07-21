"""Health check endpoints."""

from fastapi import APIRouter, Request

from app.validations.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
    include_in_schema=False,
)


@router.get("/")
async def health_check(request: Request) -> HealthResponse:
    """Health check endpoint.

    Returns the health status of the service.
    """
    return HealthResponse(
        version=request.app.version,
    )

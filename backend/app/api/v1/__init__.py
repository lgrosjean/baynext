"""API v1 module"""

from datetime import datetime, UTC

from fastapi import APIRouter, Request, Security

from app.api.v1 import datasets, jobs, me, pipelines
from app.core.security import check_token

router = APIRouter(
    prefix="/v1",
)

project_router = APIRouter(
    prefix="/projects/{project_id}",
    dependencies=[
        Security(check_token),
    ],
)

project_router.include_router(pipelines.router)
project_router.include_router(datasets.router)
project_router.include_router(jobs.router)


@router.get("/health", include_in_schema=True)
async def health_check(request: Request):
    """
    Health check endpoint.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC),
        "version": getattr(request.app, "version"),
    }


router.include_router(project_router)
router.include_router(me.router, tags=["auth"])

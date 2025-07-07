"""API v1 module"""

from fastapi import APIRouter, Security

from app.api.v1 import datasets, jobs, pipelines
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


@router.get("/health", include_in_schema=False)
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}


router.include_router(project_router)

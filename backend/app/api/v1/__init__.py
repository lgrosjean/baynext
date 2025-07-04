"""API v1 module"""

from fastapi import APIRouter, Security

from app.core.security import check_token

from . import datasets, jobs, pipelines

router = APIRouter(
    prefix="/v1/projects/{project_id}",
    dependencies=[
        Security(check_token),
    ],
)

router.include_router(pipelines.router)
router.include_router(datasets.router)
router.include_router(jobs.router)


@router.get("/health", include_in_schema=False)
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

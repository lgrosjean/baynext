"""API routes for managing project pipelines."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.core.dependencies import CurrentUserDep, SessionDep
from app.schemas.pipeline import PipelineCreate, PipelinePublic
from app.services import PipelineService

router = APIRouter(
    prefix="/pipelines",
    tags=["Pipelines"],
)


class PermissionDeniedError(HTTPException):
    """Custom exception for permission denied errors."""

    def __init__(self, reason: str) -> None:
        """Initialize the exception with a specific reason."""
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=reason)


def get_pipeline_service(
    project_id: Annotated[
        str,
        Path(description="The ID of the project", example="proj-123"),
    ],
    session: SessionDep,
    current_user: CurrentUserDep,
) -> PipelineService:
    """Dependency to get the pipeline service for a specific project."""
    pipeline_service = PipelineService(session=session, project_id=project_id)
    if not pipeline_service.project_id:
        raise PermissionDeniedError(
            reason=f"Project with ID {project_id} not found or access denied.",
        )


PipelineServiceDeps = Annotated[PipelineService, Depends(get_pipeline_service)]


@router.post(
    "",
    name="pipelines:create",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new pipeline",
    response_description="Pipeline created successfully",
)
async def create_pipeline(
    pipeline_create: PipelineCreate,
    pipeline_service: PipelineServiceDeps,
) -> PipelinePublic:
    """Create a Pipeline."""
    try:
        return await pipeline_service.create_pipeline(pipeline_create)
    except Exception as exc:
        # Handle exceptions as needed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    summary="List all pipelines in a project",
    name="pipelines:list",
)
async def list_pipelines(pipeline_service: PipelineServiceDeps) -> list[PipelinePublic]:
    """List all Pipelines."""
    try:
        return pipeline_service.list_pipelines()
    except Exception as exc:
        # Handle exceptions as needed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


# TODO(@lgrosjean): create, delete

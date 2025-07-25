"""API endpoints for managing datasets within a project."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.core.dependencies import CurrentUserDep, ProjectServiceDep
from app.schemas.dataset import DatasetPublic
from app.schemas.project import Project
from app.services import DatasetService

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


async def get_dataset_service(
    project_id: Annotated[
        str,
        Path(description="The ID of the project", example="proj-123"),
    ],
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
) -> Project:
    """Dependency to get the current active project."""
    project = project_service.get_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden to this project",
        )

    return DatasetService(session=project_service.session, project_id=project.id)


@router.get("/")
async def list_datasets(
    dataset_service: Annotated[DatasetService, Depends(get_dataset_service)],
    limit: int = 100,
    offset: int = 0,
) -> list[DatasetPublic]:
    """List all datasets for a project."""
    return dataset_service.list_datasets(limit=limit, offset=offset)

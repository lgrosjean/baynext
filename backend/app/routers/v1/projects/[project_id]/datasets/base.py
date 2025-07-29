"""Datasets endpoints for managing datasets within a project."""

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import (
    CurrentProjectMembershipDep,
    CurrentUserDep,
    SessionDep,
)
from app.core.logging import get_logger
from app.models.dataset import DatasetCreate, DatasetCreated
from app.services import DatasetService

logger = get_logger(__name__)

router = APIRouter(tags=["Datasets"], prefix="/datasets")


@router.post(
    "",
    status_code=201,
    summary="Create a new dataset",
)
async def create_dataset(
    current_user: CurrentUserDep,
    current_project_membership: CurrentProjectMembershipDep,
    dataset_data: DatasetCreate,
    session: SessionDep,
) -> DatasetCreated:
    """Create a new dataset for the current authenticated user."""
    project, _ = current_project_membership
    return DatasetService(session, project_id=project.id).create(
        dataset_data,
        user_id=current_user.id,
    )


@router.get(
    "",
    summary="List all datasets in the project",
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - User does not have access to this project",
        },
    },
)
async def list_dataset_projects(
    current_project_membership: CurrentProjectMembershipDep,
    session: SessionDep,
    limit: int | None = None,
    offset: int | None = None,
) -> list[DatasetCreated]:
    """List datasets for the current authenticated user."""
    project, _ = current_project_membership
    try:
        dataset_service = DatasetService(session, project_id=project.id)
        return dataset_service.list_project_datasets(
            limit=limit or 100,
            offset=offset or 0,
        )
    except Exception as e:
        logger.exception(
            "Failed to list datasets for project %s",
            project.id,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list datasets: {type(e).__name__} - {str(e)}",
        ) from e

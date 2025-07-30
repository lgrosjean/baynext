"""Datasets endpoints for managing datasets within a project."""

from typing import Annotated

from fastapi import APIRouter, File, HTTPException, status

from app.core.dependencies import (
    CurrentProjectMembershipDep,
    CurrentUserDep,
    SessionDep,
)
from app.core.logging import get_logger
from app.models.dataset import DatasetCreate, DatasetCreated, DatasetPublic
from app.services import DatasetService

logger = get_logger(__name__)

router = APIRouter(tags=["Dataset"])


@router.post(
    "/",
    status_code=201,
    summary="Create a new dataset",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Dataset created successfully",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error - Failed to create dataset",
        },
    },
)
async def create_dataset(
    current_user: CurrentUserDep,
    current_project_membership: CurrentProjectMembershipDep,
    dataset_data: Annotated[
        DatasetCreate,
        File(),
    ],  # https://stackoverflow.com/a/79585735
    session: SessionDep,
) -> DatasetCreated:
    """Create a new dataset in the specified project.

    You can obtain a `project_id` by listing the projects for your Baynext account.

    """
    project, _ = current_project_membership

    try:
        return await DatasetService(session, project_id=project.id).create(
            dataset_data,
            user_id=current_user.id,
        )
    except Exception as e:
        logger.exception("Failed to create dataset in project %s", project.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create dataset: {type(e).__name__} - {e!s}",
        ) from e


@router.get(
    "/",
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
) -> list[DatasetPublic]:
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

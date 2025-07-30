"""Datasets endpoints for managing datasets within a project."""

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import (
    CurrentProjectMembershipDep,
    SessionDep,
)
from app.core.logging import get_logger
from app.models.dataset import DatasetDetails
from app.services import DatasetService

logger = get_logger(__name__)

router = APIRouter(tags=["Dataset"], prefix="/{dataset_id}")


@router.get(
    "",
    summary="Retrieve dataset details",
    response_model_exclude_none=True,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - User does not have access to this project",
        },
    },
)
async def get_dataset_details(
    current_project_membership: CurrentProjectMembershipDep,
    session: SessionDep,
    dataset_id: str,
) -> DatasetDetails:
    """Get details for a specific dataset.

    You can obtain a `project_id` by listing the projects for your Baynext account.
    You can obtain a `dataset_id` by listing the project's datasets.
    A `dataset_id` value has a `ds-` prefix.

    """
    project, _ = current_project_membership
    try:
        return DatasetService(session, project_id=project.id).get_by_id(
            dataset_id=dataset_id,
        )
    except Exception as exc:
        logger.exception(
            "Failed to retrieve dataset %s for project %s: %s",
            dataset_id,
            project.id,
            exc,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve dataset: {type(exc).__name__} - {str(exc)}",
        ) from exc

"""Endpoints for project management."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import (
    SessionDep,
    get_project_member_or_owner,
    require_project_admin,
)
from app.models.membership import Membership
from app.models.project import Project, ProjectDetails
from app.services import ProjectService

router = APIRouter(tags=["Project"], prefix="")


@router.get(
    "/",
    summary="Get a given project",
    response_model_exclude_none=True,
)
async def get_project(
    project_member: Annotated[
        tuple[Project, Membership],
        Depends(get_project_member_or_owner),
    ],
) -> ProjectDetails:
    """Get a specific project for the current authenticated user."""
    return project_member[0]


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
async def delete_project(
    project: Annotated[
        Project,
        Depends(require_project_admin),
    ],
    session: SessionDep,
) -> None:
    """Delete a specific project for the current authenticated user."""
    deleted = ProjectService(session).delete(project.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

"""Endpoints for project management."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import (
    SessionDep,
    get_project_member_or_owner,
    require_project_admin,
)
from app.models.membership import Membership
from app.models.project import Project, ProjectPublic
from app.services import ProjectService

router = APIRouter(tags=["Project"], prefix="/{project_id}")


@router.get(
    "",
    summary="Get a given project",
)
async def get_project(
    project_member: Annotated[
        tuple[Project, Membership],
        Depends(get_project_member_or_owner),
    ],
) -> ProjectPublic:
    """Get a specific project for the current authenticated user."""
    project, membership = project_member
    return project


@router.delete(
    "",
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

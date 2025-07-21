"""Endpoints for project management."""

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUserDep, ProjectServiceDep
from app.schemas.project import ProjectPublic

router = APIRouter(tags=["Project"])


@router.get(
    "/",
    summary="Get a given project",
)
async def get_project(
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
    project_id: str,
) -> ProjectPublic:
    """Get a specific project for the current authenticated user."""
    project = project_service.get_user_project(current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
async def delete_project(
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
    project_id: str,
) -> None:
    """Delete a specific project for the current authenticated user."""
    project = project_service.get_user_project(current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_service.delete(project.id)

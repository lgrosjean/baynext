"""API v1 module for project management."""

from typing import Annotated

from fastapi import APIRouter, Query

from app.core.dependencies import CurrentUserDep, SessionDep
from app.models.project import ProjectCreate, ProjectCreated, ProjectPublic
from app.services import ProjectService

router = APIRouter(tags=["Project"])


@router.get(
    "/",
    summary="List all projects a user is a member of",
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
async def list_user_projects(
    current_user: CurrentUserDep,
    session: SessionDep,
    limit: Annotated[
        int | None,
        Query(example=10, gt=0, lt=100, description="Number of projects to return"),
    ] = None,
    offset: Annotated[
        int | None,
        Query(example=0, description="Number of projects to skip"),
    ] = None,
) -> list[ProjectPublic]:
    """List projects for the current authenticated user."""
    project_service = ProjectService(session)
    return project_service.list_user_projects(
        user_id=current_user.id,
        limit=limit or 100,
        offset=offset or 0,
    )


@router.post(
    "/",
    status_code=201,
    summary="Create a new project",
)
async def create(
    current_user: CurrentUserDep,
    project_data: ProjectCreate,
    session: SessionDep,
) -> ProjectCreated:
    """Create a new project for the current authenticated user."""
    return ProjectService(session).create(project_data, user_id=current_user.id)

"""API v1 module for project management."""

from fastapi import APIRouter

from app.core.dependencies import CurrentUserDep, ProjectServiceDep
from app.schemas.project import ProjectBase, ProjectCreate, ProjectPublic

router = APIRouter(tags=["Projects"])


@router.get(
    "/",
    summary="List all projects",
)
async def list_(
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
    limit: int = 100,
    offset: int = 0,
) -> list[ProjectPublic]:
    """List projects for the current authenticated user."""
    return project_service.list_user_projects(
        current_user.id,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/",
    status_code=201,
    summary="Create a new project",
)
async def create(
    project: ProjectBase,
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
) -> ProjectPublic:
    """Create a new project for the current authenticated user."""
    project_data = ProjectCreate(**project.model_dump(), user_id=current_user.id)
    return project_service.create(project_data)

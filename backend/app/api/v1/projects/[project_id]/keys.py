"""API routes for managing project API keys."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.core.dependencies import KeyServiceDep
from app.schemas.key import (
    KeyCreateRequest,
    KeyPublic,
    KeyResponse,
)

router = APIRouter(
    prefix="/keys",
    tags=["API Keys"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new API key",
    response_description="API key created",
)
async def create_api_key(
    key_request: KeyCreateRequest,
    key_service: KeyServiceDep,
) -> KeyPublic:
    """Create a new API key inside the project."""
    key_record, api_key = key_service.create(key_request)

    # Return the key record with the actual API key
    return KeyResponse(
        id=key_record.id,
        name=key_record.name,
        description=key_record.description,
        permissions=key_record.permissions,
        expires_at=key_record.expires_at,
        last_used_at=key_record.last_used_at,
        is_active=key_record.is_active,
        created_at=key_record.created_at,
        updated_at=key_record.updated_at,
        key=api_key,  # Only returned on creation
    )


@router.get("/")
async def list_api_keys(
    key_service: KeyServiceDep,
    skip: Annotated[
        int,
        Query(description="Number of keys to skip for pagination"),
    ] = 0,
    limit: Annotated[int, Query(description="Maximum number of keys to return")] = 100,
    *,
    # Making show_inactive a query parameter keyword-only argument
    show_inactive: Annotated[
        bool,
        Query(
            description="Whether to include inactive keys in the list",
            alias="showInactive",
        ),
    ] = False,
) -> list[KeyPublic]:
    """List all API keys for a project."""
    return key_service.list_(skip=skip, limit=limit, show_inactive=show_inactive)


@router.get("/{key_id}")
async def get_api_key(
    project_id: str,
    key_id: str,
    key_service: KeyServiceDep,
) -> KeyResponse:
    """Get a specific API key for a project."""
    key = key_service.get_by_id(key_id)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    if key.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found in this project",
        )

    return key


@router.delete(
    "/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an API key",
    response_description="API key deleted",
)
async def delete_api_key(
    project_id: str,
    key_id: str,
    key_service: KeyServiceDep,
) -> None:
    """Delete an API key."""
    # Check that the API key exists and belongs to this project
    if not key_service.is_key_in_project(key_id, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found in this project",
        )
    deleted = key_service.delete(key_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )


# @router.post("/{key_id}/deactivate")
# async def deactivate_api_key()

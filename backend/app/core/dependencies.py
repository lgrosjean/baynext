"""Defines dependencies for FastAPI routes."""

from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery, OAuth2PasswordBearer
from sqlmodel import Session

from app.core.db import get_session
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_jwt_token
from app.schemas.user import User
from app.services import DatasetService, ProjectService, UserService
from app.services.key import KeyService

_API_KEY_HEADER = "x-baynext-api-key"
"""Header name for API key authentication."""

_API_KEY_QUERY = "key"
"""Query parameter name for API key authentication."""

SessionDep = Annotated[Session, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    """Dependency to get a UserService instance.

    Args:
        session: SQLModel database session for operations

    Returns:
        UserService: An instance of UserService initialized with the session

    """
    return UserService(session=session)


def get_project_service(session: SessionDep) -> ProjectService:
    """Dependency to get a ProjectService instance.

    Args:
        session: SQLModel database session for operations

    Returns:
        ProjectService: An instance of ProjectService initialized with the session

    """
    return ProjectService(session=session)


def get_dataset_service(session: SessionDep) -> DatasetService:
    """Dependency to get a DatasetService instance.

    Args:
        session: SQLModel database session for operations

    Returns:
        DatasetService: An instance of DatasetService initialized with the session
        and project ID.

    """
    return DatasetService(session=session)


def get_key_service(session: SessionDep, project_id: str) -> KeyService:
    """Dependency to get a KeyService instance.

    Args:
        project_id: ID of the project for which to manage keys
        session: SQLModel database session for operations

    Returns:
        KeyService: An instance of KeyService initialized with the session

    """
    return KeyService(session=session, project_id=project_id)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
DatasetServiceDep = Annotated[DatasetService, Depends(get_dataset_service)]
KeyServiceDep = Annotated[KeyService, Depends(get_key_service)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="v1/auth/token",
    scheme_name="Bearer",
    description="JWT Bearer token for authentication",
    refreshUrl="v1/auth/token/refresh",
    auto_error=False,
)


def get_current_user(
    user_service: UserServiceDep,
    token: str = Depends(oauth2_scheme),
) -> User:
    """Dependency to get the currently authenticated user.

    This function retrieves the current user from the UserService.

    Args:
        user_service: An instance of UserService
        token: The JWT token from the request

    Returns:
        User: The currently authenticated user

    Raises:
        UnauthorizedError: If the user is not authenticated

    """
    payload = decode_jwt_token(token)
    user_id = payload.get("sub")
    user = user_service.get_by_id(user_id)
    if not user:
        message = "User is not authenticated"
        raise UnauthorizedError(message)
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
"""Dependency to get the currently authenticated user."""


async def check_jwt(
    token: str = Depends(oauth2_scheme),
) -> None:
    """Verify the JWT token in the request."""
    try:
        decode_jwt_token(token)
    except Exception as exc:
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired JWT token",
        ) from exc


query_scheme = APIKeyQuery(name=_API_KEY_QUERY, auto_error=False)


class NotMatchedProjectError(HTTPException):
    """Custom exception for project ID mismatch with API key."""

    def __init__(self, project_id: str) -> None:
        """Initialize the NotMatchedProjectError with a project ID."""
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"API key does not match the project ID: {project_id}",
        )


async def check_api_key_in_query(
    api_key: Annotated[str, Depends(query_scheme)],
    key_service: KeyServiceDep,
    project_id: str,
) -> None:
    """Verify the key in the query parameters."""
    key_found = key_service.get_by_value(api_key)
    if not key_found:
        # If the key is not found, raise an HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Key query parameter invalid",
        )
    # If the key is valid, continue processing the request
    if key_found.project_id != project_id:
        raise NotMatchedProjectError(project_id)


header_scheme = APIKeyHeader(name=_API_KEY_HEADER, auto_error=False)


async def check_api_key_in_header(
    api_key: Annotated[str, Depends(header_scheme)],
    key_service: KeyServiceDep,
    project_id: str,
) -> None:
    """Verify the API key in the request header."""
    key_found = key_service.get_by_value(api_key)
    if not key_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-baynext-api-key header invalid",
        )
    if key_found.project_id != project_id:
        raise NotMatchedProjectError(project_id)


async def check_auth(
    api_key_headers: Annotated[str, Depends(header_scheme)],
    api_key_query: Annotated[str, Depends(query_scheme)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    """Check authentication credentials in the request."""
    if token:
        await check_jwt(token)
    elif api_key_headers:
        await check_api_key_in_header(api_key_headers)
    elif api_key_query:
        await check_api_key_in_query(api_key_query)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No authentication credentials provided",
        )


CheckAuthDeps = Security(check_auth)

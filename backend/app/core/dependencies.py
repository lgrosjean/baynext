"""Defines dependencies for FastAPI routes."""

from typing import Annotated
from uuid import uuid4

from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.core.db import get_session
from app.core.exceptions import UnauthorizedError
from app.core.logging import get_logger
from app.models import Membership, Project, User
from app.models.enums import UserRole
from app.services import AuthService, UserService

ProjectId = Annotated[
    str,
    Path(
        # description="Project ID",
        example=f"{uuid4()!s}",
    ),
]

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="v1/auth/token",
    scheme_name="Bearer",
    description="JWT Bearer token for authentication",
    refreshUrl="v1/auth/token/refresh",
    auto_error=False,
)


SessionDep = Annotated[Session, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    """Dependency to get a UserService instance.

    Args:
        session: SQLModel database session for operations

    Returns:
        UserService: An instance of UserService initialized with the session

    """
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
"""Dependency to get a UserService instance."""


def get_current_user(
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Get the currently authenticated user.

    This function retrieves the current user from the UserService using
    the provided JWT token.

    Args:
        session: SQLModel database session for operations
        token: The JWT token from the request

    Returns:
        User: The currently authenticated user

    Raises:
        UnauthorizedError: If the user is not authenticated

    """
    payload = AuthService.decode_jwt_token(token)
    user_id = payload.get("sub")
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        message = "User is not authenticated"
        raise UnauthorizedError(message)
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
"""Dependency to get the currently authenticated user."""


def get_project_member_or_owner(
    project_id: ProjectId,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> tuple[Project, Membership | None]:
    """Get project and user's membership (if any)."""
    project_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found",
    )

    access_denied = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied to this project",
    )

    # Get project
    project = session.exec(select(Project).where(Project.id == project_id)).first()

    if not project:
        raise project_not_found

    # Check if user is owner
    if project.owner_id == current_user.id:
        return project, None

    # Check if user is member
    member_statement = select(Membership).where(
        Membership.project_id == project_id,
        Membership.user_id == current_user.id,
    )
    member_result = session.exec(member_statement)
    membership = member_result.first()

    if not membership:
        logger.warning(
            "User %s tried to access project %s without membership",
            current_user.id,
            project_id,
        )
        raise access_denied

    return project, membership


def require_project_admin(
    project_id: ProjectId,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> Project:
    """Require user to be project owner or admin."""
    admin_access_required = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required",
    )

    project, membership = get_project_member_or_owner(
        project_id,
        current_user,
        session,
    )

    # Owner has admin rights
    if project.owner_id == current_user.id:
        logger.info(
            "🔐 User %s is the owner of project %s", current_user.id, project_id
        )
        return project

    # Check if user is admin member
    if membership and membership.role == UserRole.ADMIN:
        logger.info("🔐 User %s is an admin of project %s", current_user.id, project_id)
        return project

    raise admin_access_required


def require_project_editor(
    project_id: ProjectId,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> Project:
    """Require user to be project owner, admin, or editor."""
    editor_access_required = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Editor access required",
    )

    project, membership = get_project_member_or_owner(
        project_id,
        current_user,
        session,
    )

    # Owner has all rights
    if project.owner_id == current_user.id:
        return project

    # Check if user has editor or admin rights
    if membership and membership.role in [UserRole.ADMIN, UserRole.EDITOR]:
        return project

    raise editor_access_required


# from fastapi.security import APIKeyHeader, APIKeyQuery,

# query_scheme = APIKeyQuery(name=_API_KEY_QUERY, auto_error=False)


# class NotMatchedProjectError(HTTPException):
#     """Custom exception for project ID mismatch with API key."""

#     def __init__(self, project_id: str) -> None:
#         """Initialize the NotMatchedProjectError with a project ID."""
#         super().__init__(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=f"API key does not match the project ID: {project_id}",
#         )


# async def check_api_key_in_query(
#     api_key: Annotated[str, Depends(query_scheme)],
#     key_service: KeyServiceDep,
#     project_id: str,
# ) -> None:
#     """Verify the key in the query parameters."""
#     key_found = key_service.get_by_value(api_key)
#     if not key_found:
#         # If the key is not found, raise an HTTPException
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Key query parameter invalid",
#         )
#     # If the key is valid, continue processing the request
#     if key_found.project_id != project_id:
#         raise NotMatchedProjectError(project_id)


# header_scheme = APIKeyHeader(name=_API_KEY_HEADER, auto_error=False)


# async def check_api_key_in_header(
#     api_key: Annotated[str, Depends(header_scheme)],
#     key_service: KeyServiceDep,
#     project_id: str,
# ) -> None:
#     """Verify the API key in the request header."""
#     key_found = key_service.get_by_value(api_key)
#     if not key_found:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="X-baynext-api-key header invalid",
#         )
#     if key_found.project_id != project_id:
#         raise NotMatchedProjectError(project_id)


# async def check_auth(
#     api_key_headers: Annotated[str, Depends(header_scheme)],
#     api_key_query: Annotated[str, Depends(query_scheme)],
#     token: Annotated[str, Depends(oauth2_scheme)],
# ) -> None:
#     """Check authentication credentials in the request."""
#     if token:
#         await check_jwt(token)
#     elif api_key_headers:
#         await check_api_key_in_header(api_key_headers)
#     elif api_key_query:
#         await check_api_key_in_query(api_key_query)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="No authentication credentials provided",
#         )


# CheckAuthDeps = Security(check_auth)

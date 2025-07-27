"""FastAPI router for user-related endpoints."""

from fastapi import APIRouter

from app.core.dependencies import CurrentUserDep
from app.models.user import UserPublic

router = APIRouter(prefix="/me")


@router.get("")
def get_current_user_details(current_user: CurrentUserDep) -> UserPublic:
    """Get the current user.

    This endpoint is used to retrieve the user information of the currently
    authenticated user.
    """
    return current_user

"""Endpoint to manage user information."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core import security

router = APIRouter(prefix="/me")


@router.get("")
def get_current_user(
    user: Annotated[security.User, Depends(security.get_current_user)],
) -> security.User:
    """Get the current user.

    This endpoint is used to retrieve the user information of the currently authenticated
    user.
    """
    return user

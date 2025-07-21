"""Authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.dependencies import CurrentUserDep, UserServiceDep
from app.core.security import create_user_jwt_token
from app.schemas.user import UserPublic

TOKEN_EXPIRATION_SECONDS = 3600  # 1 hour

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


class Token(BaseModel):
    """Model for the access token response.

    This model defines the structure of the token response returned by the `/token`
    endpoint.
    """

    access_token: str
    token_type: str


@router.post("/token", include_in_schema=False)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
) -> Token:
    """Login and return an access token."""
    user = user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_user_jwt_token(user, expiration=TOKEN_EXPIRATION_SECONDS)

    # The response of the token endpoint must be a JSON object.
    # It should have a token_type. In our case, as we are using "Bearer" tokens,
    # the token type should be "bearer". And it should have an access_token,
    # with a string containing our access token.
    # See: # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#return-the-token
    return Token(access_token=access_token, token_type="bearer")  # noqa: S106


@router.get("/me")
def get_current_user(current_user: CurrentUserDep) -> UserPublic:
    """Get the current user.

    This endpoint is used to retrieve the user information of the currently
    authenticated user.
    """
    return current_user

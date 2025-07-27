"""Authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.dependencies import SessionDep
from app.core.logging import get_logger
from app.services import AuthService

TOKEN_EXPIRATION_SECONDS = 3600  # 1 hour

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    include_in_schema=False,  # Hide from OpenAPI schema
)

logger = get_logger(__name__)


class Token(BaseModel):
    """Model for the access token response.

    This model defines the structure of the token response returned by the `/token`
    endpoint.
    """

    access_token: str
    token_type: str


@router.post("/token")
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    """Login and return an access token."""
    auth_service = AuthService(session)

    user = auth_service.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        logger.warning("🔒 User not found: %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("✅ User found: %s", user.id)

    data = {
        "sub": user.id,
        "email": user.email,
        "username": user.username,
    }

    access_token = auth_service.create_access_token(data)

    logger.info("✅ Access token created for user: %s", user.id)

    # The response of the token endpoint must be a JSON object.
    # It should have a token_type. In our case, as we are using "Bearer" tokens,
    # the token type should be "bearer". And it should have an access_token,
    # with a string containing our access token.
    # See: # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#return-the-token
    return Token(access_token=access_token, token_type="bearer")  # noqa: S106

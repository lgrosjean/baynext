import os
from base64 import b64decode
from typing import Annotated

import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from pydantic import BaseModel, EmailStr

from app.core.settings import settings
from app.core.exceptions import UnauthoriedError, AuthError


# JWT configuration
JWT_SECRET = os.getenv("AUTH_SECRET")
if not JWT_SECRET:
    raise ValueError("AUTH_SECRET environment variable is required")

ALGORITHM = "HS256"  # Adjust if you use a different algorithm


class User(BaseModel):
    id: str
    email: EmailStr
    name: str


async def check_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(
            HTTPBearer(
                description="Bearer token for API access",
            )
        ),
    ],
) -> None:
    if credentials.credentials != settings.ml_api_secret_api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(
            HTTPBearer(
                description="Bearer token for API access",
            )
        ),
    ],
) -> User:
    """Get the current user from the JWT token from the request headers."""
    if not credentials:
        raise AuthError("No credentials provided")

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            b64decode(JWT_SECRET),
            algorithms=[ALGORITHM],
        )
        user_id = payload.get("sub")
        email = payload.get("email")
        name = payload.get("name")

        if not user_id:
            raise UnauthoriedError("User ID not found in token")

        if not email:
            raise UnauthoriedError("Email not found in token")

        user = User(
            id=user_id,
            email=email,
            name=name or "",
        )
        return user

    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        ) from exc

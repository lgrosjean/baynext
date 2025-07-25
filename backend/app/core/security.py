"""Security module for handling authentication and authorization in the application."""

import os
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.core.exceptions import MissingAuthSecretError
from app.schemas.user import User

ALGORITHM = "HS256"

MISSING_USER_ID_MESSAGE = "User ID not found in token"
MISSING_EMAIL_MESSAGE = "Email not found in token"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_jwt_secret() -> str:
    """Retrieve the JWT secret from environment variables.

    This function checks for the `AUTH_SECRET` environment variable,
    which is used to sign and verify JWT tokens. If the variable is not set,
    it raises a `MissingAuthSecretError`.

    Returns:
        str: The JWT secret key.

    Raises:
        MissingAuthSecretError: If the `AUTH_SECRET` environment variable is not set.

    """
    jwt_secret = os.getenv("AUTH_SECRET")
    if not jwt_secret:
        raise MissingAuthSecretError
    return jwt_secret


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict, expiration: int | None = None) -> str:
    """Create a JWT token with the given data and optional expiration time.

    Args:
        data (dict): The payload data to include in the token.
        expiration (int | None): Optional expiration time in seconds.
        If None, the token does not expire.

    Returns:
        str: The encoded JWT token.

    """
    jwt_secret = get_jwt_secret()
    if expiration:
        data["exp"] = datetime.now(UTC) + timedelta(seconds=expiration)
    return jwt.encode(data, jwt_secret, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> dict:
    """Decode a JWT token and return the payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload data.

    Raises:
        HTTPException: If the token is invalid or expired.

    """
    jwt_secret = get_jwt_secret()
    try:
        return jwt.decode(token, jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token",
        ) from exc


def create_user_jwt_token(user: User, expiration: int | None = None) -> str:
    """Create a JWT token for the user.

    Args:
        user (User): The user for whom the token is created.
        expiration (int | None): Optional expiration time in seconds.
        If None, the token does not expire.

    Returns:
        str: The encoded JWT token.

    """
    data = {
        "sub": user.id,
        "email": user.email,
        "name": user.name or "",
    }
    return create_jwt_token(data, expiration=expiration)

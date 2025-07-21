"""Exceptions for authentication and authorization errors."""

from fastapi import status
from fastapi.exceptions import HTTPException


class ForbiddenError(HTTPException):
    """Exception raised for authentication errors."""

    def __init__(self, details: str) -> None:
        """Initialize the exception with a specific status code and detail."""
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=details,
            headers={"WWW-Authenticate": "Bearer"},
        )


class MissingCredentialsError(ForbiddenError):
    """Exception raised when no credentials are provided."""

    def __init__(self) -> None:
        """Initialize the exception with a specific message."""
        super().__init__("No credentials provided. Please provide a valid token.")


class UnauthorizedError(HTTPException):
    """Exception raised for unauthorized access."""

    def __init__(self, details: str) -> None:
        """Initialize the exception with a specific status code and detail."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=details,
            headers={"WWW-Authenticate": "Bearer"},
        )


class MissingAuthSecretError(HTTPException):
    """Exception raised when the authentication secret is missing."""

    def __init__(self) -> None:
        """Initialize the exception with a specific status code and detail."""
        # This is a critical error, so we use 500 Internal Server Error
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AUTH_SECRET is not set in the environment variables.",
        )

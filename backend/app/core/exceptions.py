from fastapi.exceptions import HTTPException
from fastapi import status


class AuthError(HTTPException):
    """Exception raised for authentication errors."""

    def __init__(self, details):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=details,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthoriedError(HTTPException):
    """Exception raised for unauthorized access."""

    def __init__(self, details):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=details,
            headers={"WWW-Authenticate": "Bearer"},
        )

"""Authentication related models."""

from pydantic import BaseModel


class Token(BaseModel):
    """Model for authentication token."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105
    expires_in: int


class TokenData(BaseModel):
    """Model for token data."""

    user_id: str | None = None
    email: str | None = None

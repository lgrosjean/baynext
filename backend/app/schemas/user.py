"""User schema for database operations."""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .project import Project


class UserBase(SQLModel):
    """Base user model with common fields."""

    name: str | None = None
    email: EmailStr
    image: str | None = None


class User(UserBase, table=True):
    """User model for database storage."""

    __tablename__ = "user"

    id: str = Field(primary_key=True)
    email_verified: datetime | None = Field(
        default=None,
        alias="emailVerified",
        sa_column_kwargs={"name": "emailVerified"},
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    projects: list["Project"] = Relationship(back_populates="user")

    class Config:
        """Pydantic configuration."""

        validate_by_name = True


class UserCreate(UserBase):
    """User creation model."""

    id: str


class UserPublic(UserBase):
    """Public user model for API responses."""

    id: str
    created_at: datetime


class UserUpdate(SQLModel):
    """User update model."""

    name: str | None = None
    image: str | None = None

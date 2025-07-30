"""User model using SQLModel."""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr, field_validator
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin, UUIDMixin
from .enums import UserStatus

if TYPE_CHECKING:
    from .dataset import Dataset
    from .membership import Membership
    from .project import Project


class UserBase(SQLModel):
    # email: EmailStr
    username: str
    # first_name: str
    # last_name: str

    @classmethod
    @field_validator("username")
    def username_alphanumeric(cls, v):
        assert v.replace("_", "").replace("-", "").isalnum(), (
            "Username must be alphanumeric (with _ or - allowed)"
        )
        assert len(v) >= 3, "Username must be at least 3 characters"
        return v


class User(UserBase, UUIDMixin, TimestampMixin, table=True):
    """User model."""

    __tablename__ = "users"

    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    hashed_password: str = Field(max_length=255)
    first_name: str = Field(default=None, max_length=100)
    last_name: str = Field(default=None, max_length=100)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    last_login: datetime | None = Field(default=None)

    # Relationships
    created_projects: list["Project"] | None = Relationship(back_populates="owner")
    project_memberships: list["Membership"] | None = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "[Membership.user_id]",
        },
    )
    datasets: list["Dataset"] | None = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "foreign_keys": "[Dataset.created_by]",
        },
    )

    class Config:
        """Pydantic configuration."""

        # Enable ORM mode for Pydantic compatibility
        from_attributes = True


class UserPublic(UserBase):
    """Public user model for API responses."""

    id: str
    status: UserStatus

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserDetails(UserBase):
    """Detailed user model for API responses."""

    email: EmailStr
    username: str
    first_name: str | None = None
    last_name: str | None = None
    last_login: datetime | None = None
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        orm_mode = True
        use_enum_values = True

"""Project model using SQLModel."""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin, UUIDMixin
from .membership import MembershipPublic
from .user import UserPublic

if TYPE_CHECKING:
    from .membership import Membership
    from .user import User

DESCRIPTION_MAX_LENGTH = 1000

PROJECT_NAME_MIN_LENGTH = 3
PROJECT_NAME_MAX_LENGTH = 200


class ProjectBase(SQLModel):
    """Base project model with common fields."""

    name: str = Field(
        max_length=PROJECT_NAME_MAX_LENGTH,
        min_length=PROJECT_NAME_MIN_LENGTH,
        index=True,
    )
    description: str | None = Field(default=None, max_length=DESCRIPTION_MAX_LENGTH)

    @classmethod
    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate project name is not empty and has length constraints."""
        empty_project_name_error = ValueError("Project name cannot be empty")
        name_too_short_error = ValueError("Project name must be at least 3 characters")
        name_too_long_error = ValueError("Project name cannot exceed 200 characters")

        """Validate project name is not empty and has length constraints."""
        if not v or not v.strip():
            raise empty_project_name_error
        # Additional constraints can be added here
        if not len(v.strip()) >= PROJECT_NAME_MIN_LENGTH:
            raise name_too_short_error
        if not len(v.strip()) <= PROJECT_NAME_MAX_LENGTH:
            raise name_too_long_error
        return v.strip()

    @classmethod
    @field_validator("description")
    def validate_description(cls, v: str | None) -> str | None:
        """Validate project description is not empty and has length constraints."""
        description_too_long_error = ValueError(
            f"Project description cannot exceed {DESCRIPTION_MAX_LENGTH} characters",
        )
        if v is not None and len(v.strip()) == 0:
            return None
        if v is not None and len(v.strip()) > DESCRIPTION_MAX_LENGTH:
            raise description_too_long_error
        return v.strip() if v else None


class Project(ProjectBase, UUIDMixin, TimestampMixin, table=True):
    """Project model with SQLModel."""

    __tablename__ = "projects"

    owner_id: str = Field(foreign_key="users.id", index=True)
    """Owner ID of the project."""

    # Relationships
    owner: "User" = Relationship(back_populates="created_projects")
    members: list["Membership"] = Relationship(back_populates="project")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        str_strip_whitespace = True


class ProjectCreate(ProjectBase):
    """Project creation model for API requests."""


class ProjectCreated(ProjectBase):
    """Project creation model with owner ID."""

    id: str


class ProjectPublic(ProjectCreated):
    """Public project model for API responses."""

    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class ProjectDetail(ProjectPublic):
    """Detailed project model for API responses, including owner and members."""

    owner: UserPublic
    members: list[MembershipPublic] = []

    class Config:
        """Pydantic configuration."""

        from_attributes = True

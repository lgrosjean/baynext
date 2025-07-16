"""Project schema for database operations and API responses."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .dataset import Dataset
    from .pipeline import Pipeline
    from .user import User


# Error messages as constants
PROJECT_NAME_EMPTY_ERROR = "Project name cannot be empty"


class ProjectBase(SQLModel):
    """Base project model with common fields."""

    name: str = Field(min_length=1, max_length=255, description="Project name")
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Project description",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate project name is not empty."""
        if not v or not v.strip():  # to prevent empty strings with whitespace
            raise ValueError(PROJECT_NAME_EMPTY_ERROR)
        return v.strip()


class Project(ProjectBase, table=True):
    """Project model for database storage."""

    __tablename__ = "projects"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique project identifier",
    )
    user_id: str = Field(
        foreign_key="user.id",
        index=True,
        description="Owner user ID",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Project creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Project last update timestamp",
    )

    # Relationships
    user: Optional["User"] = Relationship(back_populates="projects")
    datasets: list["Dataset"] = Relationship(
        back_populates="project",
        cascade_delete=True,
    )
    pipelines: list["Pipeline"] = Relationship(
        back_populates="project",
        cascade_delete=True,
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        str_strip_whitespace = True


class ProjectCreate(ProjectBase):
    """Project creation model for API requests."""

    user_id: str = Field(description="Owner user ID")


class ProjectUpdate(SQLModel):
    """Project update model for API requests."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Project name",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Project description",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """Validate project name."""
        if v is not None and (not v or not v.strip()):
            raise ValueError(PROJECT_NAME_EMPTY_ERROR)
        return v.strip() if v else None


class ProjectPublic(ProjectBase):
    """Public project model for API responses."""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class ProjectWithDetails(ProjectPublic):
    """Project model with related entities for detailed API responses."""

    datasets_count: int = Field(default=0, description="Number of datasets")
    pipelines_count: int = Field(default=0, description="Number of pipelines")
    last_activity: datetime | None = Field(
        default=None,
        description="Last activity timestamp",
    )


class ProjectListResponse(SQLModel):
    """Response model for project list endpoints."""

    projects: list[ProjectPublic]
    total: int
    page: int
    size: int
    has_next: bool

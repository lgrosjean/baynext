"""Dataset model for defining datasets database schmema and validation."""

import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from pydantic import Field as PydanticField
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin, UUIDMixin
from app.models.enums import KpiType

if TYPE_CHECKING:
    from .project import Project
    from .user import User

from .user import UserPublic


class DatasetBase(SQLModel):
    """Base dataset model for shared attributes."""

    display_name: str = PydanticField(
        min_length=1,
        max_length=255,
        description="Display name for the dataset",
        examples=["Q3 Media Performance Dataset"],
        alias="displayName",
    )

    kpi_type: KpiType = PydanticField(
        description="Type of KPI (revenue or non-revenue)",
        alias="kpiType",
    )


class Dataset(DatasetBase, UUIDMixin, TimestampMixin, table=True):
    """Dataset model for database storage."""

    __tablename__ = "datasets"

    project_id: str = Field(
        foreign_key="projects.id",
        index=True,
        description="Parent project ID",
    )

    created_by: str = Field(
        foreign_key="users.id",
        description="User ID of the dataset creator",
    )

    blob_path: str = Field(
        max_length=255,
        description="Path to the dataset blob storage",
    )

    last_modified_by: str | None = Field(
        default=None,
        foreign_key="users.id",
        description="User ID of the last modifier",
    )

    # Relationships
    creator: "User" = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Dataset.created_by]",
        },
        back_populates="datasets",
    )
    last_modifier: "User" = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Dataset.last_modified_by]",
        },
    )
    project: "Project" = Relationship(back_populates="datasets")

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        use_enum_values = True
        validate_assignment = True
        str_strip_whitespace = True


class DatasetCreate(DatasetBase):
    """Dataset creation model for API requests."""


class DatasetCreated(DatasetCreate):
    """Dataset created model for API responses."""

    id: str = PydanticField(
        description="Unique identifier for the dataset",
        examples=[f"{uuid4()!s}"],
    )
    project_id: str = PydanticField(
        description="Parent project ID",
        alias="projectId",
        examples=[f"{uuid4()!s}"],
    )

    class Config:
        populate_by_name = True
        use_enum_values = True


class DatasetDetails(DatasetCreated):
    """Detailed dataset model for API responses."""

    display_name: str = PydanticField(
        description="Display name for the dataset",
        alias="displayName",
    )
    creator: UserPublic = PydanticField(
        description="User who created the dataset",
        alias="createdBy",
    )

    kpi_type: KpiType = PydanticField(
        description="Type of KPI (revenue or non-revenue)",
        alias="kpiType",
    )
    blob_path: str = PydanticField(
        description="Path to the dataset blob storage",
        alias="blobPath",
    )
    created_at: datetime.datetime = PydanticField(
        description="Timestamp when the dataset was created",
        alias="createdAt",
    )
    last_modified_by: str | None = PydanticField(
        default=None,
        description="User ID of the last modifier",
        alias="lastModifiedBy",
    )

    class Config:
        populate_by_name = True
        use_enum_values = True

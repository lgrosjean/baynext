"""Dataset schema for database operations and API responses."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, HttpUrl, ValidationInfo, field_validator
from sqlmodel import (
    ARRAY,
    JSON,
    AutoString,
    Field,
    Relationship,
    SQLModel,
    String,
)
from sqlmodel import Enum as SQLEnum

from app.schemas.enums import KpiType

if TYPE_CHECKING:
    from .pipeline import Pipeline
    from .project import Project

_PREFIX = "ds_"


class DatasetBase(SQLModel):
    """Base dataset model with common fields."""

    name: str = Field(min_length=1, max_length=255, description="Dataset name")
    time: str = Field(min_length=1, max_length=100, description="Time column name")
    kpi: str = Field(min_length=1, max_length=100, description="KPI column name")
    kpi_type: KpiType = Field(description="Type of KPI (revenue or non-revenue)")

    # Optional fields
    geo: str | None = Field(
        default=None,
        max_length=100,
        description="Geographic column name",
    )
    population: str | None = Field(
        default=None,
        max_length=100,
        description="Population column name",
    )
    revenue_per_kpi: str | None = Field(
        default=None,
        max_length=100,
        description="Revenue per KPI column name",
    )

    # Array fields
    controls: list[str] | None = Field(
        default=None,
        description="Control variables list",
    )
    medias: list[str] | None = Field(
        default=None,
        description="Media channels list",
    )
    media_spend: list[str] | None = Field(
        default=None,
        description="Media spend columns list",
    )

    # JSON mapping fields
    media_to_channel: dict[str, str] | None = Field(
        default=None,
        description="Mapping of media to channels",
    )
    media_spend_to_channel: dict[str, str] | None = Field(
        default=None,
        description="Mapping of media spend to channels",
    )

    @field_validator("name", "time", "kpi")
    @classmethod
    def validate_required_strings(cls, v: str, info: ValidationInfo) -> str:
        """Validate required string fields."""
        if not v or not v.strip():
            field_name = info.field_name.replace("_", " ").title()
            msg = f"{field_name} cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("controls", "medias", "media_spend")
    @classmethod
    def validate_string_lists(cls, v: list[str] | None) -> list[str] | None:
        """Validate string lists contain non-empty strings."""
        if v is None:
            return v
        if not isinstance(v, list):
            return v

        # Filter out empty strings and strip whitespace
        cleaned = [item.strip() for item in v if item and item.strip()]
        return cleaned if cleaned else None

    @field_validator("media_to_channel", "media_spend_to_channel")
    @classmethod
    def validate_media_mappings(cls, v: dict[str, str] | None) -> dict[str, str] | None:
        """Validate media mappings."""
        if v is None:
            return v
        if not isinstance(v, dict):
            return v

        # Validate that all keys and values are non-empty strings
        cleaned = {}
        for key, value in v.items():
            if not key or not key.strip() or not value or not value.strip():
                continue
            cleaned[key.strip()] = value.strip()

        return cleaned if cleaned else None


class Dataset(DatasetBase, table=True):
    """Dataset model for database storage."""

    __tablename__ = "datasets"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique dataset identifier",
    )
    project_id: str = Field(
        foreign_key="projects.id",
        index=True,
        description="Parent project ID",
    )
    file_url: str = Field(
        sa_type=AutoString,
        description="Dataset file URL",
    )
    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Dataset upload timestamp",
    )

    # Override base fields with SQLAlchemy types
    kpi_type: KpiType = Field(
        sa_type=SQLEnum(
            KpiType,
            name="kpi_type",
            values_callable=lambda x: [e.value for e in x],
        ),
        description="Type of KPI (revenue or non-revenue)",
    )
    controls: list[str] | None = Field(
        default=None,
        sa_type=ARRAY(String),
        description="Control variables list",
    )
    medias: list[str] | None = Field(
        default=None,
        sa_type=ARRAY(String),
        description="Media channels list",
    )
    media_spend: list[str] | None = Field(
        default=None,
        sa_type=ARRAY(String),
        description="Media spend columns list",
    )
    media_to_channel: dict | None = Field(
        default=None,
        sa_type=JSON,
        description="Mapping of media to channels",
    )
    media_spend_to_channel: dict | None = Field(
        default=None,
        sa_type=JSON,
        description="Mapping of media spend to channels",
    )

    # Relationships
    project: Optional["Project"] = Relationship(back_populates="datasets")
    pipelines: list["Pipeline"] = Relationship(
        back_populates="dataset",
        cascade_delete=True,
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        str_strip_whitespace = True


class DatasetCreate(DatasetBase):
    """Dataset creation model for API requests."""

    project_id: str = Field(description="Parent project ID")
    file_url: str = Field(description="Dataset file URL")

    @field_validator("file_url")
    @classmethod
    def validate_file_url(cls, v: str) -> str:
        """Validate that file_url is a valid URL."""
        if not v or not v.strip():
            msg = "File URL cannot be empty"
            raise ValueError(msg)

        # Validate as HttpUrl but return as string for database compatibility
        try:
            validated_url = HttpUrl(v.strip())
            return str(validated_url)
        except Exception as e:
            msg = f"Invalid URL format: {e}"
            raise ValueError(msg) from e


class DatasetUpdate(SQLModel):
    """Dataset update model for API requests."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Dataset name",
    )
    time: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Time column name",
    )
    kpi: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="KPI column name",
    )
    kpi_type: KpiType | None = Field(
        default=None,
        description="Type of KPI (revenue or non-revenue)",
    )
    geo: str | None = Field(
        default=None,
        max_length=100,
        description="Geographic column name",
    )
    population: str | None = Field(
        default=None,
        max_length=100,
        description="Population column name",
    )
    revenue_per_kpi: str | None = Field(
        default=None,
        max_length=100,
        description="Revenue per KPI column name",
    )
    controls: list[str] | None = Field(
        default=None,
        description="Control variables list",
    )
    medias: list[str] | None = Field(
        default=None,
        description="Media channels list",
    )
    media_spend: list[str] | None = Field(
        default=None,
        description="Media spend columns list",
    )
    media_to_channel: dict[str, str] | None = Field(
        default=None,
        description="Mapping of media to channels",
    )
    media_spend_to_channel: dict[str, str] | None = Field(
        default=None,
        description="Mapping of media spend to channels",
    )

    @field_validator("name", "time", "kpi")
    @classmethod
    def validate_optional_strings(
        cls,
        v: str | None,
        info: ValidationInfo,
    ) -> str | None:
        """Validate optional string fields."""
        if v is not None and (not v or not v.strip()):
            field_name = info.field_name.replace("_", " ").title()
            msg = f"{field_name} cannot be empty"
            raise ValueError(msg)
        return v.strip() if v else None


class DatasetPublic(BaseModel):
    """Public dataset model for API responses."""

    name: str = Field(
        description="Dataset name",
        schema_extra={
            "examples": ["Sales Data Q1 2023", "Marketing Campaign Dataset"],
        },
    )

    id: str = Field(
        description="Unique dataset identifier",
        schema_extra={
            "examples": ["dataset-123"],
        },
    )
    project_id: str = Field(
        description="Parent project ID",
        schema_extra={
            "examples": ["proj-123"],
        },
    )
    file_url: HttpUrl
    uploaded_at: datetime

    @field_validator("file_url", mode="before")
    @classmethod
    def validate_url_for_output(cls, v: str | HttpUrl) -> HttpUrl:
        """Convert string URL to HttpUrl for API responses."""
        if isinstance(v, HttpUrl):
            return v
        return HttpUrl(v)


class DatasetWithDetails(DatasetPublic):
    """Dataset model with related entities for detailed API responses."""

    pipelines_count: int = Field(default=0, description="Number of pipelines")
    file_size: int | None = Field(default=None, description="File size in bytes")
    row_count: int | None = Field(default=None, description="Number of data rows")
    last_accessed: datetime | None = Field(
        default=None,
        description="Last access timestamp",
    )


class DatasetListResponse(SQLModel):
    """Response model for dataset list endpoints."""

    datasets: list[DatasetPublic]
    total: int
    page: int
    size: int
    has_next: bool

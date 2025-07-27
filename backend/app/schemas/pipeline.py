"""Pipeline schemas for database and validation."""

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pydantic import Field as PydanticField
from pydantic import field_validator
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel

from app.schemas.dataset import _PREFIX as DATASET_PREFIX
from app.validations.model_spec import ModelSpec

if TYPE_CHECKING:
    from .dataset import Dataset
    from .job import Job
    from app.models.project import Project


_PREFIX = "pipe_"

INVALID_DATASET_ID_FORMAT_ERROR = "dataset_id must be a valid UUID"


class PipelineBase(SQLModel):
    """Base pipeline model for shared attributes."""

    display_name: str = PydanticField(
        min_length=1,
        max_length=255,
        description="Display name for the pipeline",
        examples=["Q3 Media Performance Pipeline"],
        alias="displayName",
    )
    dataset_id: str = PydanticField(
        examples=[f"{DATASET_PREFIX}{uuid.uuid4()!s}"],
        description="ID of the dataset this pipeline operates on",
        alias="datasetId",
    )


class Pipeline(SQLModel, table=True):
    """Pipeline model."""

    __tablename__ = "pipelines"

    id: str | None = Field(
        default_factory=lambda: f"{_PREFIX}{uuid.uuid4()!s}",
        primary_key=True,
    )
    project_id: str = Field(foreign_key="projects.id")
    dataset_id: str = Field(foreign_key="datasets.id")

    model_spec: ModelSpec = Field(sa_column=Column(JSONB))

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationship
    project: "Project" = Relationship(back_populates="pipelines")
    dataset: "Dataset" = Relationship(back_populates="pipelines")
    jobs: list["Job"] | None = Relationship(back_populates="pipeline")

    @field_validator("model_spec")
    def val_model_spec(cls, val) -> "ModelSpec":
        """Validate model_spec is a valid ModelSpec."""
        return val.dict()


class PipelineCreate(PipelineBase):
    """Pipeline creation model."""

    model_spec: ModelSpec

    @field_validator("dataset_id")
    @classmethod
    def validate_dataset_id(cls, v: str) -> str:
        """Validate dataset_id is a valid UUID."""
        try:
            uuid.UUID(v)
        except ValueError as exc:
            raise ValueError(INVALID_DATASET_ID_FORMAT_ERROR) from exc
        return v


class PipelinePublic(PipelineBase):
    """Public pipeline model for API responses."""

    id: str = PydanticField(
        examples=[f"{_PREFIX}{uuid.uuid4()!s}"],
        description="Unique identifier for the pipeline",
    )
    created_at: datetime = PydanticField(
        description="Timestamp when the pipeline was created",
        alias="createdAt",
    )

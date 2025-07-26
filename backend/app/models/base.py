"""Base model configurations for SQLModel."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlmodel import Field


class TimestampMixin:
    """Mixin for timestamp fields."""

    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
        index=True,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"onupdate": datetime.now(UTC)},
    )


class UUIDMixin:
    """Mixin for UUID primary key."""

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )

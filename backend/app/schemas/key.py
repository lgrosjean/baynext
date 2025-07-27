"""API Key schema for database operations and API responses."""

import secrets
import uuid
from datetime import UTC, datetime, timedelta

from sqlmodel import Field, SQLModel

_PREFIX = "key_"

# TODO(@lgrosjean): Create permissions (write, delete, read)


class KeyBase(SQLModel):
    """Base API key model with common fields."""

    description: str = Field(
        min_length=1,
        max_length=255,
        description="Description of the API key purpose",
        schema_extra={
            "examples": [
                "Production API access",
                "Development testing",
                "CI/CD pipeline",
            ],
        },
    )
    expires_at: datetime | None = Field(
        default=None,
        description="Expiration date of the API key. If None, key never expires.",
    )


class Key(KeyBase, table=True):
    """API Key model for database storage."""

    __tablename__ = "api_key"

    id: str = Field(
        default_factory=lambda: f"{_PREFIX}{uuid.uuid4()!s}",
        primary_key=True,
        description="Unique identifier for the API key",
    )
    project_id: str = Field(
        foreign_key="projects.id",
        description="ID of the project that owns this API key",
    )
    key: str = Field(
        default_factory=lambda: f"byn_{secrets.token_urlsafe(32)}",
        description="Hashed version of the API key for security",
        index=True,
    )
    is_active: bool = Field(
        default=True,
        description="Whether the API key is active and can be used",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the API key was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the API key was last updated",
    )

    # Relationships
    # project: "Project" = Relationship(back_populates="api_keys")

    @property
    def is_expired(self) -> bool:
        """Check if the API key has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(datetime.UTC) > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if the API key is valid (active and not expired)."""
        return self.is_active and not self.is_expired


class KeyCreate(KeyBase):
    """API key creation model."""

    project_id: str


class KeyPublic(SQLModel):
    """Public API key model for API responses (without sensitive data)."""

    id: str = Field(
        description="Unique identifier for the API key",
        schema_extra={"examples": ["key_12345"]},
    )
    description: str = Field(
        description="Description of the API key purpose",
        schema_extra={"examples": ["API key description"]},
    )
    expires_at: datetime | None = Field(
        schema_extra={"serialization_alias": "expiresAt"},
    )
    is_active: bool = Field(
        description="Whether the API key is currently active",
        schema_extra={"serialization_alias": "isActive"},
    )
    created_at: datetime = Field(
        description="Timestamp when the API key was created",
        schema_extra={"serialization_alias": "createdAt"},
    )
    updated_at: datetime = Field(
        description="Timestamp when the API key was last updated",
        schema_extra={"serialization_alias": "updatedAt"},
    )

    @property
    def is_expired(self) -> bool:
        """Check if the API key has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(datetime.UTC) > self.expires_at


class KeyResponse(KeyPublic):
    """API key response model that includes the actual key (only on creation)."""

    key: str | None = Field(
        default=None,
        description="The actual API key (only returned on creation)",
    )


class KeyUpdate(SQLModel):
    """API key update model."""

    description: str | None = None
    expires_at: datetime | None = None
    is_active: bool | None = None


class KeyCreateRequest(SQLModel):
    """API key creation request model."""

    description: str = Field(
        min_length=1,
        max_length=255,
        description="Description of the API key purpose",
        schema_extra={
            "examples": [
                "Production API access",
                "Development testing",
                "CI/CD pipeline",
            ],
        },
    )
    expires_in_days: int | None = Field(
        default=30,
        ge=1,
        le=365,
        description="Number of days until the key expires (default: 30, max: 365)",
    )

    def to_key_create(self, project_id: str) -> KeyCreate:
        """Convert to KeyCreate with calculated expiration date."""
        expires_at = None
        if self.expires_in_days:
            expires_at = datetime.now(datetime.UTC) + timedelta(
                days=self.expires_in_days,
            )

        return KeyCreate(
            description=self.description,
            expires_at=expires_at,
            project_id=project_id,
        )

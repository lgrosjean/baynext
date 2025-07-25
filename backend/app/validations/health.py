"""Health validation module.

This module defines the health check response model and status enumeration.
"""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    """Health status enumeration."""

    OK = "ok"
    ERROR = "error"


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: HealthStatus = Field(
        default=HealthStatus.OK,
        description="Health status of the service",
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    version: str = Field(examples=["x.y.z"])

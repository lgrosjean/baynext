# app/models/dataset.py

from datetime import datetime
from typing import Optional

from pydantic import UUID4, HttpUrl
from sqlmodel import ARRAY, JSON, AutoString, Field, SQLModel, String


class DatasetPublic(SQLModel):
    """Public dataset schema for API responses."""

    id: UUID4
    project_id: str
    name: str
    file_url: HttpUrl = Field(sa_type=AutoString)

    uploaded_at: datetime


class DatasetDetailsPublic(DatasetPublic):
    """Public dataset schema for detailed API responses."""

    geo: Optional[str] = None
    time: str
    kpi: str

    kpi_type: str | None = None  # If you have enum later, can tighten

    population: Optional[str] = None
    revenue_per_kpi: Optional[str] = None

    # Array fields
    controls: Optional[list[str]] = Field(default=None, sa_type=ARRAY(String))
    medias: Optional[list[str]] = Field(default=None, sa_type=ARRAY(String))
    media_spend: Optional[list[str]] = Field(default=None, sa_type=ARRAY(String))

    # JSON fields
    media_to_channel: Optional[dict] = Field(default=None, sa_type=JSON)
    media_spend_to_channel: Optional[dict] = Field(default=None, sa_type=JSON)

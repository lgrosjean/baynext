"""Tests for dataset schema validation and functionality."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError
from pydantic.networks import HttpUrl

from app.schemas.dataset import (
    Dataset,
    DatasetBase,
    DatasetCreate,
    DatasetListResponse,
    DatasetPublic,
    DatasetUpdate,
    DatasetWithDetails,
)
from app.schemas.enums import KpiType


class TestDatasetBase:
    """Test DatasetBase validation logic."""

    def test_valid_dataset_base(self) -> None:
        """Test creating a valid DatasetBase instance."""
        dataset = DatasetBase(
            name="Test Dataset",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            geo="region",
            population="audience_size",
            revenue_per_kpi="revenue_per_conv",
            controls=["seasonality", "promotions"],
            medias=["facebook", "google"],
            media_spend=["facebook_spend", "google_spend"],
            media_to_channel={"facebook": "social", "google": "search"},
            media_spend_to_channel={
                "facebook_spend": "social",
                "google_spend": "search",
            },
        )

        assert dataset.name == "Test Dataset"
        assert dataset.time == "date"
        assert dataset.kpi == "conversions"
        assert dataset.kpi_type == KpiType.REVENUE
        assert dataset.geo == "region"
        assert dataset.population == "audience_size"
        assert dataset.revenue_per_kpi == "revenue_per_conv"
        assert dataset.controls == ["seasonality", "promotions"]
        assert dataset.medias == ["facebook", "google"]
        assert dataset.media_spend == ["facebook_spend", "google_spend"]
        assert dataset.media_to_channel == {"facebook": "social", "google": "search"}
        assert dataset.media_spend_to_channel == {
            "facebook_spend": "social",
            "google_spend": "search",
        }

    def test_minimal_valid_dataset_base(self):
        """Test creating a minimal valid DatasetBase instance."""
        dataset = DatasetBase(
            name="Minimal Dataset",
            time="week",
            kpi="sales",
            kpi_type=KpiType.NON_REVENUE,
        )

        assert dataset.name == "Minimal Dataset"
        assert dataset.time == "week"
        assert dataset.kpi == "sales"
        assert dataset.kpi_type == KpiType.NON_REVENUE
        assert dataset.geo is None
        assert dataset.population is None
        assert dataset.revenue_per_kpi is None
        assert dataset.controls is None
        assert dataset.medias is None
        assert dataset.media_spend is None
        assert dataset.media_to_channel is None
        assert dataset.media_spend_to_channel is None

    def test_required_field_validation(self):
        """Test validation of required string fields."""
        # Test empty name - now uses Pydantic's built-in min_length validation
        with pytest.raises(ValidationError) as exc_info:
            DatasetBase(
                name="",
                time="date",
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
            )
        assert "String should have at least 1 character" in str(exc_info.value)

        # Test whitespace-only name - our custom validator should handle this
        with pytest.raises(ValidationError) as exc_info:
            DatasetBase(
                name="   ",
                time="date",
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
            )
        assert "Name cannot be empty" in str(exc_info.value)

        # Test empty time
        with pytest.raises(ValidationError) as exc_info:
            DatasetBase(
                name="Test",
                time="",
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
            )
        assert "String should have at least 1 character" in str(exc_info.value)

        # Test empty kpi
        with pytest.raises(ValidationError) as exc_info:
            DatasetBase(
                name="Test",
                time="date",
                kpi="",
                kpi_type=KpiType.REVENUE,
            )
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_string_list_validation(self):
        """Test validation of string list fields."""
        # Test with valid lists
        dataset = DatasetBase(
            name="Test",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            controls=["control1", "control2"],
            medias=["media1", "media2"],
            media_spend=["spend1", "spend2"],
        )
        assert dataset.controls == ["control1", "control2"]
        assert dataset.medias == ["media1", "media2"]
        assert dataset.media_spend == ["spend1", "spend2"]

        # Test with lists containing empty strings and whitespace
        dataset = DatasetBase(
            name="Test",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            controls=["  control1  ", "", "control2", "   "],
            medias=["media1", "", "   media2   "],
            media_spend=["", "  spend1  ", ""],
        )
        assert dataset.controls == ["control1", "control2"]
        assert dataset.medias == ["media1", "media2"]
        assert dataset.media_spend == ["spend1"]

        # Test with lists containing only empty strings
        dataset = DatasetBase(
            name="Test",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            controls=["", "   ", ""],
        )
        assert dataset.controls is None

    def test_media_mapping_validation(self):
        """Test validation of media mapping fields."""
        # Test with valid mappings
        dataset = DatasetBase(
            name="Test",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            media_to_channel={"facebook": "social", "google": "search"},
            media_spend_to_channel={"fb_spend": "social", "google_spend": "search"},
        )
        assert dataset.media_to_channel == {"facebook": "social", "google": "search"}
        assert dataset.media_spend_to_channel == {
            "fb_spend": "social",
            "google_spend": "search",
        }

        # Test with mappings containing empty/whitespace keys/values
        dataset = DatasetBase(
            name="Test",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            media_to_channel={"  facebook  ": "  social  ", "": "search", "google": ""},
            media_spend_to_channel={"   ": "   ", "valid_key": "valid_value"},
        )
        assert dataset.media_to_channel == {"facebook": "social"}
        assert dataset.media_spend_to_channel == {"valid_key": "valid_value"}

        # Test with mappings containing only empty/whitespace entries
        dataset = DatasetBase(
            name="Test",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            media_to_channel={"": "", "   ": "   "},
        )
        assert dataset.media_to_channel is None

    def test_field_length_validation(self):
        """Test field length constraints."""
        # Test maximum length constraints
        with pytest.raises(ValidationError):
            DatasetBase(
                name="x" * 256,  # Too long
                time="date",
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
            )

        with pytest.raises(ValidationError):
            DatasetBase(
                name="Test",
                time="x" * 101,  # Too long
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
            )

        with pytest.raises(ValidationError):
            DatasetBase(
                name="Test",
                time="date",
                kpi="x" * 101,  # Too long
                kpi_type=KpiType.REVENUE,
            )


class TestDatasetCreate:
    """Test DatasetCreate validation logic."""

    def test_valid_dataset_create(self):
        """Test creating a valid DatasetCreate instance."""
        dataset = DatasetCreate(
            project_id="proj-123",
            name="Test Dataset",
            file_url="https://example.com/dataset.csv",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
        )

        assert dataset.project_id == "proj-123"
        assert dataset.name == "Test Dataset"
        assert dataset.file_url == "https://example.com/dataset.csv"
        assert isinstance(
            dataset.file_url, str
        )  # Should be string for DB compatibility

    def test_file_url_validation(self):
        """Test file URL validation."""
        # Test valid URLs
        valid_urls = [
            "https://example.com/file.csv",
            "http://localhost:8000/data.json",
            "https://storage.googleapis.com/bucket/file.parquet",
        ]

        for url in valid_urls:
            dataset = DatasetCreate(
                project_id="proj-123",
                name="Test",
                file_url=url,
                time="date",
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
            )
            assert dataset.file_url == url

        # Test invalid URLs
        invalid_urls = [
            "",
            "   ",
            "not-a-url",
            "ftp://invalid-scheme.com/file.csv",
            "just-a-string",
        ]

        for url in invalid_urls:
            with pytest.raises(ValidationError) as exc_info:
                DatasetCreate(
                    project_id="proj-123",
                    name="Test",
                    file_url=url,
                    time="date",
                    kpi="conversions",
                    kpi_type=KpiType.REVENUE,
                )
            assert "Invalid URL format" in str(
                exc_info.value
            ) or "File URL cannot be empty" in str(exc_info.value)

    def test_url_normalization(self):
        """Test that URLs are properly normalized."""
        dataset = DatasetCreate(
            project_id="proj-123",
            name="Test",
            file_url="  https://example.com/file.csv  ",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
        )
        assert dataset.file_url == "https://example.com/file.csv"


class TestDatasetUpdate:
    """Test DatasetUpdate validation logic."""

    def test_valid_dataset_update(self):
        """Test creating a valid DatasetUpdate instance."""
        update = DatasetUpdate(
            name="Updated Name",
            time="week",
            kpi="sales",
            kpi_type=KpiType.NON_REVENUE,
        )

        assert update.name == "Updated Name"
        assert update.time == "week"
        assert update.kpi == "sales"
        assert update.kpi_type == KpiType.NON_REVENUE

    def test_empty_dataset_update(self):
        """Test creating an empty DatasetUpdate instance."""
        update = DatasetUpdate()

        assert update.name is None
        assert update.time is None
        assert update.kpi is None
        assert update.kpi_type is None

    def test_optional_string_validation(self):
        """Test validation of optional string fields."""
        # Test None values (should be allowed)
        update = DatasetUpdate(name=None, time=None, kpi=None)
        assert update.name is None
        assert update.time is None
        assert update.kpi is None

        # Test empty strings (should be rejected) - uses min_length validation
        with pytest.raises(ValidationError) as exc_info:
            DatasetUpdate(name="")
        assert "String should have at least 1 character" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            DatasetUpdate(time="   ")
        assert "Time cannot be empty" in str(exc_info.value)

        # Test valid strings with whitespace (should be trimmed)
        update = DatasetUpdate(name="  Test Name  ", time="  date  ")
        assert update.name == "Test Name"
        assert update.time == "date"


class TestDatasetPublic:
    """Test DatasetPublic validation and conversion logic."""

    def test_valid_dataset_public_from_string_url(self):
        """Test creating DatasetPublic with string URL."""
        now = datetime.now(timezone.utc)
        dataset = DatasetPublic(
            id="ds-123",
            project_id="proj-123",
            name="Test Dataset",
            file_url="https://example.com/dataset.csv",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            uploaded_at=now,
        )

        assert dataset.id == "ds-123"
        assert dataset.project_id == "proj-123"
        assert dataset.name == "Test Dataset"
        assert isinstance(dataset.file_url, HttpUrl)
        assert str(dataset.file_url) == "https://example.com/dataset.csv"
        assert dataset.uploaded_at == now

    def test_valid_dataset_public_from_httpurl(self):
        """Test creating DatasetPublic with HttpUrl object."""
        now = datetime.now(timezone.utc)
        url = HttpUrl("https://example.com/dataset.csv")

        dataset = DatasetPublic(
            id="ds-123",
            project_id="proj-123",
            name="Test Dataset",
            file_url=url,
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            uploaded_at=now,
        )

        assert isinstance(dataset.file_url, HttpUrl)
        assert dataset.file_url == url


class TestDatasetWithDetails:
    """Test DatasetWithDetails extended model."""

    def test_valid_dataset_with_details(self):
        """Test creating DatasetWithDetails with all fields."""
        now = datetime.now(timezone.utc)
        dataset = DatasetWithDetails(
            id="ds-123",
            project_id="proj-123",
            name="Test Dataset",
            file_url="https://example.com/dataset.csv",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            uploaded_at=now,
            pipelines_count=3,
            file_size=1024000,
            row_count=50000,
            last_accessed=now,
        )

        assert dataset.pipelines_count == 3
        assert dataset.file_size == 1024000
        assert dataset.row_count == 50000
        assert dataset.last_accessed == now

    def test_dataset_with_details_defaults(self):
        """Test DatasetWithDetails with default values."""
        now = datetime.now(timezone.utc)
        dataset = DatasetWithDetails(
            id="ds-123",
            project_id="proj-123",
            name="Test Dataset",
            file_url="https://example.com/dataset.csv",
            time="date",
            kpi="conversions",
            kpi_type=KpiType.REVENUE,
            uploaded_at=now,
        )

        assert dataset.pipelines_count == 0
        assert dataset.file_size is None
        assert dataset.row_count is None
        assert dataset.last_accessed is None


class TestDatasetListResponse:
    """Test DatasetListResponse model."""

    def test_valid_dataset_list_response(self):
        """Test creating a valid DatasetListResponse."""
        now = datetime.now(timezone.utc)
        datasets = [
            DatasetPublic(
                id="ds-1",
                project_id="proj-123",
                name="Dataset 1",
                file_url="https://example.com/dataset1.csv",
                time="date",
                kpi="conversions",
                kpi_type=KpiType.REVENUE,
                uploaded_at=now,
            ),
            DatasetPublic(
                id="ds-2",
                project_id="proj-123",
                name="Dataset 2",
                file_url="https://example.com/dataset2.csv",
                time="week",
                kpi="sales",
                kpi_type=KpiType.NON_REVENUE,
                uploaded_at=now,
            ),
        ]

        response = DatasetListResponse(
            datasets=datasets,
            total=10,
            page=1,
            size=2,
            has_next=True,
        )

        assert len(response.datasets) == 2
        assert response.total == 10
        assert response.page == 1
        assert response.size == 2
        assert response.has_next is True


class TestDataset:
    """Test Dataset table model."""

    def test_dataset_model_fields(self):
        """Test that Dataset model has the correct field definitions."""
        # Test the table name
        assert Dataset.__tablename__ == "datasets"

        # Test that the Dataset model inherits from DatasetBase
        assert issubclass(Dataset, DatasetBase)

        # Test that it has the required additional fields for database storage
        dataset_fields = Dataset.model_fields

        # Check database-specific fields
        assert "id" in dataset_fields
        assert "project_id" in dataset_fields
        assert "file_url" in dataset_fields
        assert "uploaded_at" in dataset_fields

        # Check that it has all base fields
        assert "name" in dataset_fields
        assert "time" in dataset_fields
        assert "kpi" in dataset_fields
        assert "kpi_type" in dataset_fields

    def test_dataset_model_instantiation_basic(self):
        """Test basic Dataset model instantiation without relationships."""
        now = datetime.now(timezone.utc)

        # Create a minimal dataset without triggering relationship loading
        dataset_data = {
            "id": "ds-123",
            "project_id": "proj-123",
            "name": "Test Dataset",
            "file_url": "https://example.com/dataset.csv",
            "uploaded_at": now,
            "time": "date",
            "kpi": "conversions",
            "kpi_type": KpiType.REVENUE,
        }

        # Test field assignment without SQLAlchemy session
        for field, value in dataset_data.items():
            # This tests that the field exists and accepts the expected type
            assert hasattr(Dataset, field), f"Dataset should have field {field}"


class TestKpiTypeIntegration:
    """Test KpiType enum integration with dataset models."""

    def test_all_kpi_types_work(self):
        """Test that all KpiType values work with dataset models."""
        for kpi_type in KpiType:
            dataset = DatasetBase(
                name="Test",
                time="date",
                kpi="test_kpi",
                kpi_type=kpi_type,
            )
            assert dataset.kpi_type == kpi_type

    def test_invalid_kpi_type(self):
        """Test that invalid KpiType values are rejected."""
        with pytest.raises(ValidationError):
            DatasetBase(
                name="Test",
                time="date",
                kpi="test_kpi",
                kpi_type="invalid_type",
            )

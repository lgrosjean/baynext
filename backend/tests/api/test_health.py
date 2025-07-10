from unittest.mock import patch
from datetime import datetime as dt, UTC

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.api.v1.datetime")  # This patches the imported 'datetime' class
def test_health_check(mock_datetime_class):
    # Create a mock datetime object that will be JSON serializable

    # Use a real datetime object so FastAPI can serialize it properly
    fixed_datetime = dt(2023, 10, 1, 12, 0, 0)

    # Mock the datetime.now() class method to return our fixed datetime
    mock_datetime_class.now.return_value = fixed_datetime

    response = client.get("/v1/health")

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "ok"

    # FastAPI will serialize the datetime to ISO format
    assert result["timestamp"] == "2023-10-01T12:00:00"
    assert result["version"] == app.version

    # Verify that datetime.now was called with UTC
    mock_datetime_class.now.assert_called_once_with(UTC)

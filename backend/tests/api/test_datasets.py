from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.db import get_session
from app.core.security import check_token
from app.main import app

PROJECT_ID = "proj-123"
TOKEN = "ml_api_secret_api_key"


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def client(mock_session):
    """
    Fixture that provides a TestClient instance for testing FastAPI endpoints with overridden dependencies.

    This fixture overrides the `get_session` and `check_token` dependencies of the FastAPI app to use a mock database session and bypass authentication, respectively. It yields a TestClient configured with an authorization header for use in tests. After the test, it resets the dependency overrides to their original state.

    Args:
        mock_session: A mock database session to be used in place of the real session.

    Yields:
        TestClient: An instance of FastAPI's TestClient with overridden dependencies for testing.
    """
    # Override dependencies
    app.dependency_overrides[get_session] = lambda: mock_session
    app.dependency_overrides[check_token] = lambda: None

    client_ = TestClient(
        app,
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    yield client_

    # Clean up
    app.dependency_overrides = {}


@pytest.fixture
def expected_datasets():
    dataset_id_1 = str(uuid4())
    dataset_id_2 = str(uuid4())
    return [
        {
            "id": dataset_id_1,
            "project_id": PROJECT_ID,
            "name": "Dataset 1",
            "file_url": "https://example.com/dataset1.csv",
            "uploaded_at": datetime.now().isoformat(),
        },
        {
            "id": dataset_id_2,
            "project_id": PROJECT_ID,
            "name": "Dataset 2",
            "file_url": "https://example.com/dataset2.csv",
            "uploaded_at": datetime.now().isoformat(),
        },
    ]


@pytest.mark.asyncio
@patch("app.api.v1.datasets.DatasetService")
async def test_list_datasets_success(
    mock_dataset_service,
    client,
    mock_session,
    expected_datasets,
):
    # Arrange
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.list.return_value = expected_datasets

    # Act
    response = client.get(f"/v1/projects/{PROJECT_ID}/datasets")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_datasets
    mock_dataset_service.assert_called_once_with(mock_session, PROJECT_ID)
    mock_service_instance.list.assert_called_once()


@pytest.mark.asyncio
@patch("app.api.v1.datasets.DatasetService")
async def test_list_datasets_empty(mock_dataset_service, client):
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.list.return_value = []

    response = client.get(f"/v1/projects/{PROJECT_ID}/datasets")

    assert response.status_code == 200
    assert response.json() == []

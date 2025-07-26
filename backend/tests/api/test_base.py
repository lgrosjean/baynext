from datetime import UTC
from datetime import datetime as dt
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.core.settings import settings

client = TestClient(app)


def test_base_check():
    response = client.get("/v1/")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["message"] == settings.APP_NAME
    assert result["version"] == settings.VERSION
    assert result["authentication"] == "Bearer Token required"

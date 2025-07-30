from fastapi import status
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.main import app

client = TestClient(app)


def test_base_check():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["message"] == settings.APP_NAME
    assert result["version"] == settings.VERSION
    assert result["authentication"] == "Bearer Token required"

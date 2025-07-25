"""API client for Baynext CLI."""

import logging
from typing import Any

import httpx
import typer
from rich.logging import RichHandler

from baynext_cli.config import get_api_url, get_token

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


ERROR_401_UNAUTHORIZED = "🔒 Unauthorized, please login again with `baynext auth login`"
ERROR_403_FORBIDDEN = "⛔️ Forbidden"
ERROR_404_NOT_FOUND = "❓ Not Found"


class APIClient:
    """Baynext API Client."""

    def __init__(self) -> None:
        """Initialize the API client."""
        self.base_url = get_api_url()
        self._token = get_token()
        self._client = httpx.Client(base_url=self.base_url)

    def get_headers(self, headers: dict[str, str] | None = None) -> dict[str, str]:
        """Get headers for API requests."""
        headers = headers or {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response."""
        try:
            if response.status_code == httpx.codes.UNAUTHORIZED:
                logger.error(ERROR_401_UNAUTHORIZED)
                raise ERROR_401_UNAUTHORIZED

            if response.status_code == httpx.codes.FORBIDDEN:
                logger.error(ERROR_403_FORBIDDEN)
                raise ERROR_403_FORBIDDEN

            if response.status_code == httpx.codes.NOT_FOUND:
                logger.error(ERROR_404_NOT_FOUND)
                raise ERROR_404_NOT_FOUND

            if not response.is_success:
                error_data = (
                    response.json()
                    if response.headers.get("content-type", "").startswith(
                        "application/json",
                    )
                    else {}
                )
                error_msg = error_data.get(
                    "detail",
                    f"HTTP {response.status_code} error",
                )
                typer.echo(f"❌ Error: {error_msg}", err=True)
                raise typer.Exit(1)

            if response.status_code == httpx.codes.NO_CONTENT:
                return {"success": True}

            return response.json()

        except httpx.HTTPError:
            logger.exception("HTTP error occurred")

    def _request(
        self,
        method: str,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make an API request."""
        with self._client as client:
            response = client.request(
                method,
                endpoint,
                json=json,
                data=data,
                headers=self.get_headers(headers),
            )
            return self._handle_response(response)

    def _post(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make POST request."""
        return self._request("POST", endpoint, json=json, data=data, headers=headers)

    def _get(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make GET request."""
        return self._request("GET", endpoint, headers=headers)

    def _put(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make PUT request."""
        return self._request("PUT", endpoint, json=data)

    def _delete(self, endpoint: str) -> dict[str, Any]:
        """Make DELETE request."""
        return self._request("DELETE", endpoint)

    def get_token(self, username: str, password: str) -> str | None:
        """Get the current access token."""
        payload = {"username": username, "password": password}
        return self._post(
            "/auth/token",
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "accept": "application/json",
            },
        )

    def me(self) -> dict[str, Any]:
        """Get current user information."""
        return self._get("/me")

    def list_projects(self) -> list[dict[str, Any]]:
        """List all projects."""
        return self._get("/projects")

    def create_project(self, name: str, description: str) -> dict[str, Any]:
        """Create a new project."""
        data = {"name": name, "description": description}
        return self._post("/projects", json=data)

    def get_project(self, project_id: str) -> dict[str, Any]:
        """Get details of a project."""
        return self._get(f"/projects/{project_id}")

    def delete_project(self, project_id: str) -> dict[str, Any]:
        """Delete a project."""
        return self._delete(f"/projects/{project_id}")

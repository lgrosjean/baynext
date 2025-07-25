"""
API client for Baynext CLI
"""

import httpx
import typer
from typing import Optional, Dict, Any
from baynext.config import get_api_url, get_token


class Client:
    def __init__(self, project_id: str):
        self.base_url = get_api_url()
        self.token = get_token()
        self.project_id = project_id

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            if response.status_code == 401:
                typer.echo(
                    "❌ Unauthorized. Please login first with: baynext auth login",
                    err=True,
                )
                raise typer.Exit(1)
            elif response.status_code == 403:
                typer.echo(
                    "❌ Access forbidden. You don't have permission for this action.",
                    err=True,
                )
                raise typer.Exit(1)
            elif response.status_code == 404:
                typer.echo("❌ Resource not found.", err=True)
                raise typer.Exit(1)
            elif not response.is_success:
                error_data = (
                    response.json()
                    if response.headers.get("content-type", "").startswith(
                        "application/json"
                    )
                    else {}
                )
                error_msg = error_data.get(
                    "detail", f"HTTP {response.status_code} error"
                )
                typer.echo(f"❌ Error: {error_msg}", err=True)
                raise typer.Exit(1)

            return response.json()
        except httpx.HTTPError as e:
            typer.echo(f"❌ Network error: {e}", err=True)
            raise typer.Exit(1)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request"""
        with httpx.Client() as client:
            response = client.post(
                f"{self.base_url}{endpoint}", json=data, headers=self._get_headers()
            )
            return self._handle_response(response)

    def get(self, endpoint: str) -> Dict[str, Any]:
        """Make GET request"""
        with httpx.Client() as client:
            response = client.get(
                f"{self.base_url}{endpoint}", headers=self._get_headers()
            )
            return self._handle_response(response)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PUT request"""
        with httpx.Client() as client:
            response = client.put(
                f"{self.base_url}{endpoint}", json=data, headers=self._get_headers()
            )
            return self._handle_response(response)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        with httpx.Client() as client:
            response = client.delete(
                f"{self.base_url}{endpoint}", headers=self._get_headers()
            )
            return self._handle_response(response)

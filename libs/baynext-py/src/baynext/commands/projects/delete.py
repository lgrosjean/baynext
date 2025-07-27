"""`baynext projects delete` command."""

from typing import Annotated

import typer

from baynext.client import APIClient

app = typer.Typer()


@app.command()
def delete(
    project_id: Annotated[
        str,
        typer.Argument(..., help="ID of the project", show_default=False),
    ],
) -> None:
    """Delete a project."""
    client = APIClient()
    client.delete_project(project_id=project_id)
    typer.echo(f"✅ Project {project_id} deleted successfully.")

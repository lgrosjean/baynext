"""`baynext projects delete` command."""

from typing import Annotated

import typer
from rich.prompt import Confirm

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
    if Confirm.ask(
        "Are you sure you want to delete the project"
        f" [bold green]{project_id}[/bold green]?\n"
        "⚠️ This action cannot be undone.",
    ):
        try:
            client = APIClient()
            client.delete_project(project_id=project_id)
            typer.echo(f"✅ Project {project_id} deleted successfully.")

        except Exception as e:
            typer.echo(f"❌ Failed to delete project {project_id}: {e}", err=True)
            raise typer.Exit(1) from e

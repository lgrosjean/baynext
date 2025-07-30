"""`baynext projects get` command."""

from typing import Annotated

import typer
from httpx import HTTPStatusError
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext.client import APIClient, ForbiddenError, NotFoundError, UnauthorizedError
from baynext.utils import OutputFormat, OutputOption

app = typer.Typer()


@app.command()
def get(
    project_id: Annotated[
        str,
        typer.Argument(..., help="ID of the project", show_default=False),
    ],
    output: OutputOption = OutputFormat.TABLE,
) -> None:
    """Get details of a project."""
    try:
        client = APIClient()
        response = client.get_project(project_id=project_id)

        if output == OutputFormat.JSON:
            print_json(data=response)

        else:
            console = Console()

            table = Table()
            table.add_column("Id")
            table.add_column("Name")
            table.add_column("Created At")

            table.add_row(
                str(response["id"]),
                response["name"],
                response["created_at"],
            )

            console.print(table)
    except UnauthorizedError as exc:
        typer.echo(exc, err=True)
    except (ForbiddenError, NotFoundError) as exc:
        typer.echo(
            "❌ You may not have permission to access this project or it may not exist.",
            err=True,
        )
        raise typer.Exit(1) from exc
    except HTTPStatusError as exc:
        typer.echo(f"HTTP error occurred: {exc}", err=True)

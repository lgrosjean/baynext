"""`baynext projects get` command."""

from typing import Annotated

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext_cli.client import APIClient
from baynext_cli.utils import OutputFormat, OutputOption

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
    client = APIClient()
    response = client.get_project(project_id=project_id)

    if output == OutputFormat.JSON:
        print_json(data=response)

    else:
        console = Console()

        table = Table()
        table.add_column("Id")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Created At")

        table.add_row(
            str(response["id"]),
            response["name"],
            response["description"],
            response["created_at"],
        )

        console.print(table)

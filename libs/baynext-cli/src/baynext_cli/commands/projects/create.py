"""`baynext projects create` command."""

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext_cli.client import APIClient
from baynext_cli.utils import OutputFormat, OutputOption

app = typer.Typer()


@app.command()
def create(
    name: str = typer.Option(..., help="Name of the project", show_default=False),
    description: str = typer.Option("", help="Description of the project"),
    output: OutputOption = OutputFormat.TABLE,
) -> None:
    """🆕 Create a new project."""
    client = APIClient()
    response = client.create_project(name=name, description=description)

    if output == OutputFormat.JSON:
        print_json(data=response)

    else:
        console = Console()

        table = Table()
        table.add_column("Id")
        table.add_column("Name")
        table.add_column("Description")

        table.add_row(
            str(response["id"]),
            response["name"],
            response["description"],
        )

        console.print(table)

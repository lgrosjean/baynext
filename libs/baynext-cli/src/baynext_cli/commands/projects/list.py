"""`baynext projects list` command."""

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext_cli.client import APIClient
from baynext_cli.utils import OutputFormat, OutputOption

app = typer.Typer()


@app.command()
def list(  # noqa: A001
    output: OutputOption = OutputFormat.TABLE,
) -> None:
    """List projects accessible by the active account."""
    client = APIClient()
    response = client.list_projects()

    if output == OutputFormat.JSON:
        print_json(data=response)

    else:
        console = Console()

        table = Table(title="📂 My projects")
        table.add_column("Project ID", style="cyan")
        table.add_column("Name", style="magenta")

        for project in response:
            table.add_row(str(project["id"]), project["name"])

        console.print(table)

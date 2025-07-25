"""`baynext auth me` commands."""

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext_cli.client import APIClient
from baynext_cli.utils import OutputFormat, OutputOption

console = Console()

table = Table()
table.add_column("ID", style="green")
table.add_column("Username", style="cyan")
table.add_column("Email", style="magenta")

app = typer.Typer()


@app.command()
def me(
    output: OutputOption = OutputFormat.TABLE,
) -> None:
    """👤 Show current user information."""
    client = APIClient()

    try:
        response = client.me()

        if output == OutputFormat.JSON:
            print_json(data=response)

        else:
            table.add_row(
                str(response["id"]),
                response["username"],
                response["email"],
            )
            console.print(table)

    except Exception as e:
        typer.echo(f"❌ Failed to fetch user info: {e}", err=True)
        raise typer.Exit(1) from e

"""`baynext datasets list` command."""

from typing import Annotated

import typer
from httpx import HTTPStatusError
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext.client import APIClient, ForbiddenError, NotFoundError, UnauthorizedError
from baynext.utils import OutputFormat, OutputOption

from .utils import get_project_id_from_ctx

app = typer.Typer()


@app.command()
def list(  # noqa: A001
    ctx: typer.Context,
    output: OutputOption = OutputFormat.TABLE,
) -> None:
    """List projects accessible by the active account."""
    project_id = get_project_id_from_ctx(ctx)
    try:
        client = APIClient()
        response = client.list_datasets(project_id=project_id)

        if output == OutputFormat.JSON:
            print_json(data=response)

        else:
            console = Console()

            table = Table()
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("KPI type")

            for dataset in response:
                table.add_row(
                    str(dataset["id"]),
                    dataset["displayName"],
                    dataset.get("kpiType", "N/A"),
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
        raise typer.Exit(1) from exc
    except Exception as e:
        typer.echo(f"❌ An unexpected error occurred: {e}", err=True)
        raise typer.Exit(1) from e
    else:
        typer.echo("✅ Datasets listed successfully.")

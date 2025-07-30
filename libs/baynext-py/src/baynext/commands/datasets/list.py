"""`baynext datasets list` command."""

from typing import Any

import typer
from httpx import HTTPStatusError
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext.client import APIClient, ForbiddenError, NotFoundError, UnauthorizedError
from baynext.commands.utils import get_project_id_from_ctx
from baynext.utils import OutputFormat, OutputOption

app = typer.Typer()


def print_table(
    data: dict[str, Any],
    columns: list[str],
    title: str | None = None,
) -> None:
    """Print a table to rich console with the given columns."""
    console = Console()
    table = Table(title=title)
    for column in columns:
        table.add_column(column, style="cyan")

    for item in data:
        row = [str(item[col]) for col in columns]
        table.add_row(*row)

    console.print(table)


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
            print_table(
                data=response,
                columns=["id", "displayName", "createdAt"],
                title="Datasets",
            )
    except UnauthorizedError as exc:
        typer.echo(exc, err=True)
    except (ForbiddenError, NotFoundError) as exc:
        typer.echo(
            "❌ You may not have permission to access this project "
            "or it may not exist.",
            err=True,
        )
        raise typer.Exit(1) from exc
    except HTTPStatusError as exc:
        typer.echo(f"HTTP error occurred: {exc}", err=True)
        raise typer.Exit(1) from exc
    except Exception as e:
        typer.echo(f"❌ An unexpected error occurred: {e}", err=True)
        raise typer.Exit(1) from e

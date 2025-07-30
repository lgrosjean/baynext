"""`baynext projects get` command."""

from typing import Annotated

import typer
from httpx import HTTPStatusError
from rich import print_json
from rich.console import Console
from rich.table import Table

from baynext.client import APIClient, ForbiddenError, NotFoundError, UnauthorizedError
from baynext.commands.utils import get_project_id_from_ctx
from baynext.utils import OutputFormat, OutputOption

app = typer.Typer()


@app.command()
def get(
    ctx: typer.Context,
    dataset_id: Annotated[
        str,
        typer.Argument(..., help="ID of the dataset"),
    ],
    output: OutputOption = OutputFormat.TABLE,
) -> None:
    """Get details of a dataset."""
    project_id = get_project_id_from_ctx(ctx)
    try:
        client = APIClient()
        response = client.get_dataset(project_id=project_id, dataset_id=dataset_id)

        if output == OutputFormat.JSON:
            print_json(data=response)

        else:
            console = Console()

            table = Table()
            table.add_column("Id")
            table.add_column("Name")
            table.add_column("Blob URL")
            table.add_column("Created By")
            table.add_column("Created At")

            table.add_row(
                str(response["id"]),
                response["displayName"],
                response["blobPath"],
                response["createdBy"]["username"],
                response["createdAt"],
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

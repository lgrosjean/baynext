"""`baynext datasets` commands."""

from typing import Annotated

import typer

from baynext.config import get_config_value

from .get import app as get_app
from .list import app as list_app

app = typer.Typer(
    name="datasets",
    help="📊 Manage your datasets",
)


@app.callback()
def datasets_callback(
    ctx: typer.Context,
    project_id: Annotated[
        str,
        typer.Option(
            "--project-id",
            "-p",
            help="ID of the project",
            show_default=True,
            envvar="BAYNEXT_PROJECT_ID",
        ),
    ] = get_config_value("project_id"),
) -> None:
    """Manage datasets within a project.

    Use this command to list, get details of, or manage datasets in your projects.
    """
    if not project_id:
        typer.echo(
            "Please specify a project ID using --project-id or -p option.", err=True
        )
        raise typer.Exit(1)

    ctx.obj = {"project_id": project_id}


app.add_typer(list_app)
app.add_typer(get_app)

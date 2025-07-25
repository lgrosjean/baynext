"""`baynext auth` commands."""

import typer

from .create import app as create_app
from .delete import app as delete_app
from .get import app as get_app
from .list import app as list_app

app = typer.Typer(
    name="projects",
    help="📂 Manage your Baynext projects",
)

app.add_typer(list_app)
app.add_typer(create_app)
app.add_typer(get_app)
app.add_typer(delete_app)

"""`baynext auth` commands."""

import typer

from .login import app as login_app
from .me import app as me_app
from .token import app as token_app

app = typer.Typer(
    name="auth",
    help="🔐 Manage Baynext CLI credentials",
)

app.add_typer(login_app)
app.add_typer(me_app)
app.add_typer(token_app)

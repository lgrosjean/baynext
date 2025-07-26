"""`baynext auth token` command."""

import typer

from baynext.config import get_token

app = typer.Typer()


@app.command()
def token() -> None:
    """🎫 Show current access token."""
    current_token = get_token()
    if current_token:
        typer.echo(current_token)
    else:
        typer.echo("No token found. Please login first.")
        raise typer.Exit(1)

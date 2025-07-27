"""`baynext config set` command."""

import typer

from baynext.config import set_config
from baynext.utils import PropertyArg

app = typer.Typer()


@app.command()
def set(property_: PropertyArg, value: str) -> None:  # noqa: A001
    """Set the value of a specific Baynext CLI property."""
    set_config(property_, value)
    typer.echo(f"✅ Property '{property_}' set to: {value}")

"""`baynext auth login` command."""

import getpass

import typer

from baynext.client import APIClient
from baynext.config import get_config_value, save_token, set_config

app = typer.Typer()


def _ask_username() -> str:
    """Prompt for username."""
    username = typer.prompt("Email or username", type=str)
    set_config("username", username)
    typer.echo(f"Updated email or username to: {username}")
    return username


def _ask_password() -> str:
    """Prompt for password."""
    password = getpass.getpass("Password: ")
    set_config("password", password)
    return password


def _ask_username_and_password() -> tuple[str, str]:
    """Prompt for username and password."""
    username = _ask_username()
    password = _ask_password()
    return username, password


@app.command()
def login(
    username: str = typer.Option(
        None,
        "--username",
        "-u",
        help="Email or username for login. If not provided, will prompt.",
    ),
    password: str = typer.Option(
        None,
        "--password",
        "-p",
        help="Password for login. If not provided, will prompt.",
    ),
) -> None:
    """🔓 Login to your account and get an access token."""
    if username and password:
        email_or_username = username
    else:
        existing_email = get_config_value("username")

        if existing_email:
            typer.echo(f"Existing email or username found: {existing_email}")
            confirm = typer.confirm("Do you want to change it?", default=False)

            if confirm:
                email_or_username, password = _ask_username_and_password()

            else:
                email_or_username = existing_email
                password = get_config_value("password")

                if not password:
                    password = _ask_password()
        else:
            email_or_username, password = _ask_username_and_password()

    client = APIClient()

    try:
        response = client.get_token(email_or_username, password)
        save_token(response["access_token"])
        typer.echo("✅ Login successful!")
    except typer.Exit:
        raise
    except Exception as e:
        typer.echo(f"❌ Login failed: {e}", err=True)
        raise typer.Exit(1) from e

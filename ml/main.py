"""Define the main CLI application for the ML module."""

from typer import Typer

from cli.training import app as training_app

app = Typer(
    name="Baynext ML",
    help="Baynext Machine Learning Module CLI",
    rich_markup_mode="rich",
    invoke_without_command=True,
    no_args_is_help=True,
)

app.add_typer(training_app, name="training", no_args_is_help=True)

if __name__ == "__main__":
    app()

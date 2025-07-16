#!/usr/bin/env python3
"""CLI script to manage database operations."""

import logging
import sys
from pathlib import Path
from typing import Annotated

import typer
from sqlmodel import Session, SQLModel, text

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from scripts.seed import clear_seed_data, seed_database  # noqa: E402

from app.core.db import engine  # noqa: E402

# Import all models to ensure they're registered with SQLModel
from app.schemas.dataset import Dataset  # noqa: E402, F401
from app.schemas.job import Job  # noqa: E402, F401
from app.schemas.model import Model  # noqa: E402, F401
from app.schemas.pipeline import Pipeline  # noqa: E402, F401
from app.schemas.project import Project  # noqa: E402, F401
from app.schemas.user import User  # noqa: E402, F401

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    help="Database management CLI for Baynext API",
    rich_markup_mode="rich",
)

# Create sub-applications for seed and db commands
seed_app = typer.Typer(help="Database seeding operations")
db_app = typer.Typer(help="Database schema operations")

# Add sub-applications to main app
app.add_typer(seed_app, name="seed")
app.add_typer(db_app, name="db")


# =============================================================================
# SEED COMMANDS
# =============================================================================


@seed_app.callback(invoke_without_command=True)
def seed_main(
    ctx: typer.Context,
    clear_first: Annotated[
        bool,
        typer.Option("--clear", "-c", help="Clear existing data before seeding"),
    ] = False,
) -> None:
    """Seed the database with sample data.

    This will create sample users, projects, and datasets for development and testing.
    Run without subcommand to perform seeding.
    """
    # If a subcommand is being called, don't execute the main logic
    if ctx.invoked_subcommand is not None:
        return

    try:
        with Session(engine) as session:
            if clear_first:
                typer.echo("🧹 Clearing existing data...")
                clear_seed_data(session)

            typer.echo("🌱 Seeding database with sample data...")
            seed_database(session)

        typer.echo(
            "✅ Database seeding completed successfully!",
            color=typer.colors.GREEN,
        )

    except Exception as e:
        typer.echo(f"❌ Seeding failed: {e}", color=typer.colors.RED, err=True)
        logger.exception("Seeding operation failed")
        raise typer.Exit(1) from e


@seed_app.command(name="clear")
def clear_seed() -> None:
    """Clear all sample data from the database.

    This will remove all users, projects, and datasets created by the seed command.
    """
    # Ask for confirmation
    if not typer.confirm("Are you sure you want to clear all seed data?"):
        typer.echo("Operation cancelled.")
        raise typer.Exit

    try:
        with Session(engine) as session:
            typer.echo("🧹 Clearing seed data...")
            clear_seed_data(session)

        typer.echo("✅ Seed data cleared successfully!", color=typer.colors.GREEN)

    except Exception as e:
        typer.echo(f"❌ Clear operation failed: {e}", color=typer.colors.RED, err=True)
        logger.exception("Clear operation failed")
        raise typer.Exit(1) from e


@seed_app.command(name="reset")
def reset_seed() -> None:
    """Reset the database by clearing and then seeding with fresh data.

    This is equivalent to running 'clear' followed by 'seed'.
    """
    # Ask for confirmation
    confirm = typer.confirm("Are you sure you want to reset all seed data?")
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Exit

    try:
        with Session(engine) as session:
            typer.echo("🧹 Clearing existing data...")
            clear_seed_data(session)

            typer.echo("🌱 Seeding database with fresh data...")
            seed_database(session)

        typer.echo(
            "✅ Database reset completed successfully!",
            color=typer.colors.GREEN,
        )

    except Exception as e:
        typer.echo(f"❌ Reset operation failed: {e}", color=typer.colors.RED, err=True)
        logger.exception("Reset operation failed")
        raise typer.Exit(1) from e


# =============================================================================
# DB COMMANDS
# =============================================================================


@db_app.command(name="create")
def create_db() -> None:
    """Create all database tables.

    This will create all tables defined in the SQLModel schemas.
    """
    try:
        typer.echo("🏗️ Creating database tables...")
        SQLModel.metadata.create_all(engine)
        typer.echo("✅ Database tables created successfully!", color=typer.colors.GREEN)

    except Exception as e:
        typer.echo(f"❌ Table creation failed: {e}", color=typer.colors.RED, err=True)
        logger.exception("Table creation failed")
        raise typer.Exit(1) from e


@db_app.command(name="drop")
def drop_db() -> None:
    """Drop all database tables.

    This will remove all tables from the database. Use with caution!
    """
    # Ask for confirmation
    confirm = typer.confirm(
        "⚠️  Are you sure you want to drop ALL database tables? "
        "This action cannot be undone!",
    )
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Exit

    try:
        typer.echo("🗑️ Dropping all database tables...")
        SQLModel.metadata.drop_all(engine)
        typer.echo("✅ All tables dropped successfully!", color=typer.colors.GREEN)

    except Exception as e:
        typer.echo(f"❌ Drop tables failed: {e}", color=typer.colors.RED, err=True)
        logger.exception("Drop tables operation failed")
        raise typer.Exit(1) from e


@db_app.command(name="reset")
def reset_db() -> None:
    """Reset the database schema by dropping and recreating all tables.

    This will drop all existing tables and recreate them with the current schema.
    All data will be lost!
    """
    # Ask for confirmation
    confirm = typer.confirm(
        "⚠️  Are you sure you want to reset the database schema? "
        "This will drop ALL tables and recreate them. All data will be lost!",
    )
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Exit

    try:
        typer.echo("🔄 Starting database schema reset...")

        with Session(engine) as session:
            typer.echo("🗑️ Dropping all database tables...")

            # Use CASCADE to handle dependencies from tables not in our metadata
            session.exec(
                text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"),
            )
            session.commit()

        typer.echo("🏗️ Creating all database tables...")
        SQLModel.metadata.create_all(engine)

        typer.echo(
            "🎉 Database schema reset completed successfully!",
            color=typer.colors.GREEN,
        )

    except Exception as e:
        typer.echo(f"❌ Schema reset failed: {e}", color=typer.colors.RED, err=True)
        logger.exception("Schema reset operation failed")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()

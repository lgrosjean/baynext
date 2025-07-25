"""Database session management for the application."""

from collections.abc import Generator

from sqlmodel import Session, create_engine

from .settings import settings

engine = create_engine(
    settings.database_url.get_secret_value().replace("postgres://", "postgresql://"),
    echo=not settings.is_prod(),
)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session.

    Yields:
        Session: A SQLModel session for database operations.

    """
    with Session(engine) as session:
        yield session

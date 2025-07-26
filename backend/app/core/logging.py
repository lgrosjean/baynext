"""Logging configuration for the application."""

import logging

from .settings import settings

logger = logging.getLogger("uvicorn.error")

logger.setLevel(
    logging.DEBUG if settings.DEBUG else logging.INFO,
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logger.getChild(name)

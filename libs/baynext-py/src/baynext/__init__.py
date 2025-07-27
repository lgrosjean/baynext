"""Baynext CLI."""

import tomllib
from pathlib import Path

with Path.open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

__version__ = pyproject["project"]["version"]


from .client import APIClient

__all__ = [
    "APIClient",
    "__version__",
]

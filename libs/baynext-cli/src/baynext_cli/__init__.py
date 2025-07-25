"""Baynext CLI."""

from pathlib import Path

import tomllib

with Path.open("pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

__version__ = pyproject["project"]["version"]

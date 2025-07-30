"""Utility functions."""

import os
from pathlib import Path


def get_blob_name(blob_path: str, *, add_random_suffix: bool) -> str:
    """Generate a blob name with an optional random suffix."""
    blob_path_ = Path(blob_path)

    if not blob_path_.suffix:
        blob_extension = ".csv"
        blob_path_ = blob_path_.with_suffix(blob_extension)
    else:
        blob_extension = blob_path_.suffix

    blob_filepath = blob_path_.parent
    blob_filename = blob_path_.stem

    if add_random_suffix:
        random_suffix = os.urandom(4).hex()
        blob_filename = f"{blob_filename}_{random_suffix}"

    return f"{blob_filepath}/{blob_filename}{blob_extension}"

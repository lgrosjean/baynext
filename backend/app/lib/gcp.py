"""Utility functions for Google Cloud Platform (GCP) interactions."""

import os
from functools import cache

from fastapi import UploadFile
from google.cloud import storage

from app.core.settings import settings
from app.utils import get_blob_name


@cache
def get_storage_client() -> storage.Client:
    """Get a Google Cloud Storage client.

    Returns:
        A storage.Client instance for interacting with GCP storage.

    """
    return storage.Client()


@cache
def get_bucket(bucket_name: str | None = None) -> storage.Bucket:
    """Get a Google Cloud Storage bucket.

    Args:
        bucket_name: The name of the GCP bucket to retrieve.
        If None, uses the bucket name from the environment variable `GCS_BUCKET`.

    Returns:
        A storage.Bucket instance for the specified bucket.

    """
    client = get_storage_client()

    if not (bucket_name := bucket_name or settings.BUCKET_NAME):
        msg = (
            "Bucket name must be provided or set in the environment "
            "variable GCS_BUCKET."
        )
        raise ValueError(msg)

    return client.bucket(bucket_name or os.getenv("GCS_BUCKET"))


def check_blob_exists(blob_name: str, bucket_name: str | None = None) -> bool:
    """Check if a blob exists in the specified GCP bucket.

    Args:
        blob_name: The name of the blob to check.
        bucket_name: The name of the GCP bucket
            (default: None, uses `GCS_BUCKET` env var).

    Returns:
        bool: True if the blob exists, False otherwise.

    """
    return get_bucket(bucket_name).blob(blob_name).exists()


def upload_content_to_blob(
    blob_name: str,
    content: bytes,
    bucket_name: str | None = None,
    content_type: str = "application/octet-stream",
) -> None:
    """Upload content to a GCP storage blob.

    Args:
        bucket_name: The name of the GCP bucket.
        blob_name: The name of the blob to create or overwrite.
        content: The content to upload as bytes.
        content_type: The MIME type of the content
            (default: "application/octet-stream").

    """
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(content, content_type=content_type)


async def upload_csv_to_blob(
    file: UploadFile,
    blob_path: str,
    *,
    bucket_name: str | None = None,
    add_random_suffix: bool = True,
    allow_overwrite: bool = False,
) -> str:
    """Upload a CSV file to a GCP storage blob.

    Args:
        file: The uploaded file to be stored.
        blob_path: The path in the blob storage where the file will be uploaded.
        bucket_name: The name of the GCP bucket
            (default: None, uses `GCS_BUCKET` env var).
        add_random_suffix: Whether to add a random suffix to the file name to avoid
            conflicts (default: `True`).
        allow_overwrite: Whether to allow overwriting an existing blob at the same path
            (default: `False`).

    Returns:
        The name of the uploaded blob.

    Raises:
        ValueError: If the file type is not supported or upload fails.

    """
    if file.content_type not in ["text/csv", "application/csv"]:
        msg = (
            f"Unsupported file type: {file.content_type}. "
            "Supported types are: text/csv, application/csv"
        )
        raise ValueError(msg)

    contents = await file.read()

    blob_name = get_blob_name(blob_path, add_random_suffix=add_random_suffix)

    if not allow_overwrite and check_blob_exists(blob_name, bucket_name=bucket_name):
        msg = f"Blob {blob_name} already exists and overwrite is not allowed."
        raise ValueError(msg)

    upload_content_to_blob(
        blob_name=blob_name,
        content=contents,
        bucket_name=bucket_name,
        content_type=file.content_type,
    )

    return blob_name

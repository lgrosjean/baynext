"""API router for project-related endpoints.

This module defines the API endpoints for managing resources related to a specific project.
"""

from .base import router
from .datasets import router as datasets_router

router.include_router(datasets_router)

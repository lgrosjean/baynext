"""Definition of database enumeration."""

from enum import Enum


class UserRole(str, Enum):
    """Enumeration for user roles in a project."""

    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """Enumeration for user status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class KpiType(str, Enum):
    """Enumeration for KPI types."""

    REVENUE = "revenue"
    NON_REVENUE = "non_revenue"

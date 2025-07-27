"""Define enumerations for database types."""

from enum import Enum


class KpiType(str, Enum):
    """Enumeration for KPI types."""

    REVENUE = "revenue"
    NON_REVENUE = "non_revenue"

"""Enum definitions for various types used in the Meridian model training process."""

from enum import Enum


class KPIType(str, Enum):
    """Enum for different types of KPIs."""

    REVENUE = "revenue"
    NON_REVENUE = "non-revenue"

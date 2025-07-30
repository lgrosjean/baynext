"""Project membership model."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .base import UUIDMixin
from .enums import UserRole

if TYPE_CHECKING:
    from .project import Project
    from .user import User

from .user import UserPublic


class Membership(SQLModel, UUIDMixin, table=True):
    """Project membership model."""

    __tablename__ = "memberships"

    project_id: str = Field(foreign_key="projects.id", index=True)
    """ID of the project this membership belongs to."""

    user_id: str = Field(foreign_key="users.id", index=True)
    """ID of the user who is a member of the project."""

    role: UserRole = Field(default=UserRole.VIEWER, index=True)
    """Role of the user in the project (e.g., viewer, editor, admin)."""

    invited_by: str = Field(foreign_key="users.id")
    joined_at: datetime = Field(default_factory=lambda: datetime.now(UTC), index=True)

    # Relationships
    project: "Project" = Relationship(back_populates="members")
    user: "User" = Relationship(
        back_populates="project_memberships",
        sa_relationship_kwargs={
            "foreign_keys": "[Membership.user_id]",
        },
    )
    inviter: "User" = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Membership.invited_by]",
            "post_update": True,
        },
    )

    class Config:
        """Pydantic configuration."""

        # Enable ORM mode for Pydantic compatibility
        from_attributes = True


class MembershipPublic(SQLModel):
    """Information about a project member for API responses."""

    user: UserPublic
    role: UserRole

    class Config:
        """Pydantic configuration."""

        from_attributes = True

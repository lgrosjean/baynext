"""Dataset service for managing dataset CRUD operations."""

from sqlmodel import Session, or_, select

from app.core.logging import get_logger
from app.models.membership import Membership
from app.models.project import Project, ProjectCreate, ProjectPublic

logger = get_logger(__name__)


class ProjectService:
    """Service class for managing project CRUD operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the project service with a database session.

        Args:
            session: SQLModel database session for operations
            project_id: Optional ID of the project to filter operations

        """
        self.session = session

    def create(self, project_data: ProjectCreate, user_id: str) -> Project:
        """Create a new project in the database.

        Args:
            project_data: Project creation data containing required fields
            user_id: ID of the user creating the project

        Returns:
            Project: The created project with generated timestamps

        Raises:
            Exception: If project creation fails

        """
        db_project = Project.model_validate(
            {
                **project_data.model_dump(),
                "owner_id": user_id,  # Set the owner ID from the current user
            },
        )

        self.session.add(db_project)
        self.session.commit()
        self.session.refresh(db_project)
        logger.info("🆕 Project %s created!", db_project.id)
        return db_project

    def get_by_id(self, project_id: str) -> Project | None:
        """Retrieve a project by its ID.

        Args:
            project_id: The unique identifier for the project

        Returns:
            Project if found, None otherwise

        """
        return self.session.get(Project, project_id)

    def list_user_projects(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ProjectPublic]:
        """List projects owned by a specific user.

        Args:
            user_id: User ID to filter projects by owner
            limit: Maximum number of projects to return (default: 100)
            offset: Number of projects to skip (default: 0)

        Returns:
            List of ProjectPublic objects owned by the user

        """
        query = (
            select(Project)
            .join(Membership)
            .where(
                or_(
                    Membership.user_id == user_id,
                    Project.owner_id == user_id,
                ),
            )
        )
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def delete(self, project_id: str) -> bool:
        """Delete a project from the database.

        Args:
            project_id: The unique identifier for the project

        Returns:
            True if project was deleted, False if not found

        """
        project = self.get_by_id(project_id)
        if not project:
            return False

        self.session.delete(project)
        self.session.commit()
        logger.info("🗑️ Project %s deleted!", project_id)
        return True

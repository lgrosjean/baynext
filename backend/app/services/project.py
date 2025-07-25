"""User service for managing user CRUD operations."""

from sqlmodel import Session, select

from app.schemas.project import Project, ProjectCreate, ProjectPublic, ProjectUpdate


class ProjectService:
    """Service class for managing project CRUD operations."""

    def __init__(self, session: Session) -> None:
        """Initialize the project service with a database session.

        Args:
            session: SQLModel database session for operations

        """
        self.session = session

    def create(self, project_data: ProjectCreate) -> Project:
        """Create a new project in the database.

        Args:
            project_data: Project creation data containing required fields

        Returns:
            Project: The created project with generated timestamps

        Raises:
            Exception: If project creation fails

        """
        # Convert ProjectCreate to Project model for database storage
        db_project = Project.model_validate(project_data)

        self.session.add(db_project)
        self.session.commit()
        self.session.refresh(db_project)

        return db_project

    def get_by_id(self, project_id: str) -> Project | None:
        """Retrieve a project by its ID.

        Args:
            project_id: The unique identifier for the project

        Returns:
            Project if found, None otherwise

        """
        return self.session.get(Project, project_id)

    def get_public(self, project_id: str) -> ProjectPublic | None:
        """Get a project's public information by ID.

        Args:
            project_id: The unique identifier for the project

        Returns:
            UserPublic model with safe public data, None if not found

        """
        project = self.get_by_id(project_id)
        if project:
            return ProjectPublic.model_validate(project)
        return None

    def update(
        self,
        project_id: str,
        *,
        project: ProjectUpdate,
    ) -> Project | None:
        """Update a project's information.

        Args:
            project_id: The unique identifier for the project
            project: Project update data containing fields to modify

        Returns:
            Updated Project object if successful, None if project not found

        """
        db_project = self.get_by_id(project_id)
        if not db_project:
            return None

        # Update fields from ProjectUpdate model
        # Source: https://sqlmodel.tiangolo.com/tutorial/fastapi/update/#update-the-hero-in-the-database
        project_data = project.model_dump(exclude_unset=True)
        db_project.sqlmodel_update(project_data)

        self.session.add(db_project)
        self.session.commit()
        self.session.refresh(db_project)

        return db_project

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

        return True

    def list_(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ProjectPublic]:
        """List projects with optional filtering and pagination.

        Args:
            limit: Maximum number of projects to return (default: 100)
            offset: Number of projects to skip (default: 0)

        Returns:
            List of Project objects matching the criteria

        """
        return self.session.exec(select(Project).offset(offset).limit(limit)).all()

    def list_user_projects(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ProjectPublic]:
        """List projects owned by a specific user.

        Args:
            user_id: The ID of the user whose projects to list
            limit: Maximum number of projects to return (default: 100)
            offset: Number of projects to skip (default: 0)

        Returns:
            List of ProjectPublic objects owned by the user

        """
        return self.session.exec(
            select(Project)
            .where(Project.user_id == user_id)
            .offset(offset)
            .limit(limit)
        ).all()

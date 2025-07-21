"""Dataset service module for handling dataset-related operations."""

from sqlmodel import Session, select

from app.schemas.dataset import Dataset, DatasetPublic


class DatasetService:
    """Service class for managing dataset CRUD operations."""

    def __init__(self, session: Session, project_id: str) -> None:
        """Initialize the dataset service with a database session.

        Args:
            session: SQLModel database session for operations
            project_id: The ID of the project to which datasets belong

        """
        self.session = session
        self.project_id = project_id

    def list_datasets(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[DatasetPublic]:
        """List all datasets in the database.

        Args:
            limit: Maximum number of datasets to return (default: 100)
            offset: Number of datasets to skip (default: 0)

        Returns:
            List of DatasetPublic objects

        """
        return self.session.exec(
            select(Dataset)
            .where(Dataset.project_id == self.project_id)
            .offset(offset)
            .limit(limit),
        ).all()

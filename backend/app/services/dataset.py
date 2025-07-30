"""Dataset service for managing dataset CRUD operations."""

from sqlmodel import Session, desc, select

from app.core.logging import get_logger
from app.lib.gcp import upload_csv_to_blob
from app.models.dataset import Dataset, DatasetCreate
from app.models.project import Project

logger = get_logger(__name__)


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

    async def create(self, dataset_data: DatasetCreate, user_id: str) -> Dataset:
        """Create a new dataset in the database.

        Args:
            dataset_data: Dataset creation data containing required fields
            user_id: ID of the user creating the dataset

        Returns:
            Dataset: The created dataset with generated timestamps

        Raises:
            Exception: If dataset creation fails

        """
        logger.info(
            "Creating dataset for project %s by user %s",
            self.project_id,
            user_id,
        )

        # Read file content directly into pandas
        try:
            blob_path = f"{self.project_id}/datasets/{dataset_data.file.filename}"
            blob_name = await upload_csv_to_blob(dataset_data.file, blob_path=blob_path)
        except ValueError as e:
            logger.exception("Failed to read dataset file: %s", str(e))
            raise

        # Create database record
        logger.info("Creating dataset record in database...")
        db_dataset = Dataset.model_validate(
            {
                **dataset_data.model_dump(by_alias=True, exclude={"file"}),
                "project_id": self.project_id,
                "created_by": user_id,  # Set the creator ID from the current user
                "blob_path": blob_name,  # Use the blob path from the upload
            },
        )

        self.session.add(db_dataset)
        self.session.commit()
        self.session.refresh(db_dataset)

        logger.info("🆕 Dataset %s created!", db_dataset.id)
        return db_dataset

    def get_by_id(self, dataset_id: str) -> Dataset | None:
        """Retrieve a dataset by its ID.

        Args:
            dataset_id: The unique identifier for the dataset

        Returns:
            Dataset if found, None otherwise

        """
        return self.session.get(Dataset, dataset_id)

    def list_project_datasets(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Dataset]:
        """List datasets owned by a specific user.

        Args:
            limit: Maximum number of datasets to return (default: 100)
            offset: Number of datasets to skip (default: 0)

        Returns:
            List of Dataset objects owned by the user

        """
        query = (
            select(Dataset)
            .join(Project)
            .where(Project.id == self.project_id)
            .order_by(desc(Dataset.created_at))
        )
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def delete(self, dataset_id: str) -> bool:
        """Delete a dataset from the database.

        Args:
            dataset_id: The unique identifier for the dataset

        Returns:
            True if dataset was deleted, False if not found

        """
        dataset = self.get_by_id(dataset_id)
        if not dataset:
            return False

        self.session.delete(dataset)
        self.session.commit()
        logger.info("🗑️ Dataset %s deleted!", dataset_id)
        return True

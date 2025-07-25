"""Pipeline service module for handling pipeline-related operations."""

from sqlmodel import Session, select

from app.schemas.pipeline import Pipeline, PipelineCreate


class PipelineService:
    """Service class for managing pipeline CRUD operations."""

    def __init__(self, session: Session, project_id: str) -> None:
        """Initialize the pipeline service with a database session.

        Args:
            session: SQLModel database session for operations
            project_id: The ID of the project to which pipelines belong

        """
        self.session = session
        self.project_id = project_id

    def create_pipeline(self, pipeline: PipelineCreate) -> Pipeline:
        """Create a new pipeline.

        Args:
            pipeline: The data for the new pipeline

        Returns:
            The created pipeline

        """
        pipeline_db = Pipeline.model_validate(pipeline)
        self.session.add(pipeline_db)
        self.session.commit()
        self.session.refresh(pipeline_db)
        # TODO(@lgrosjean): create job immediately
        return pipeline_db

    def list_pipelines(self) -> list[Pipeline]:
        """List all pipelines for the project.

        Returns:
            A list of pipelines

        """
        query = select(Pipeline).where(Pipeline.project_id == self.project_id)
        return self.session.exec(query).all()

from ..schemas import Dataset, Model
from .base import make_service
from .job import JobService
from .pipeline import PipelineService

DatasetService = make_service(Dataset)
ModelService = make_service(Model)

__all__ = [
    "DatasetService",
    "JobService",
    "ModelService",
    "PipelineService",
]

from ..schemas import Model
from .base import make_service
from .dataset import DatasetService
from .pipeline import PipelineService
from .project import ProjectService
from .user import UserService

ModelService = make_service(Model)

__all__ = [
    "DatasetService",
    "JobService",
    "ModelService",
    "PipelineService",
    "ProjectService",
    "UserService",
]

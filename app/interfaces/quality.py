from abc import ABC, abstractmethod
from app.schemas.pipeline import QualityResult, ImageData, ExecutionContext

class BaseQualityEvaluator(ABC):
    @abstractmethod
    def evaluate(self, image: ImageData, context: ExecutionContext) -> QualityResult:
        pass

from abc import ABC, abstractmethod
from app.schemas.pipeline import ImageData, ExecutionContext
from app.metrics.schemas import MetricsResult

class BaseMetricsCalculator(ABC):
    @abstractmethod
    def calculate(self, original: ImageData, processed: ImageData, context: ExecutionContext) -> MetricsResult:
        pass

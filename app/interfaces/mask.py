from abc import ABC, abstractmethod
from app.schemas.pipeline import DetectionResult, MaskResult, ImageData, ExecutionContext

class BaseMaskGenerator(ABC):
    @abstractmethod
    def generate(self, image: ImageData, detections: DetectionResult, context: ExecutionContext) -> MaskResult:
        pass

class BaseMaskRefiner(ABC):
    @abstractmethod
    def refine(self, mask: MaskResult, context: ExecutionContext) -> MaskResult:
        pass

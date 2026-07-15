from abc import ABC, abstractmethod
from app.schemas.pipeline import MaskResult, InpaintResult, ImageData, ExecutionContext

class BaseInpainter(ABC):
    @abstractmethod
    def inpaint(self, image: ImageData, mask: MaskResult, context: ExecutionContext) -> InpaintResult:
        pass

from app.interfaces.locator import BaseLocator
from app.schemas.pipeline import DetectionResult, ImageData, ExecutionContext
import logging

logger = logging.getLogger(__name__)

class LocatorService:
    def __init__(self, provider: BaseLocator):
        self.provider = provider

    def process(self, image: ImageData, context: ExecutionContext) -> DetectionResult:
        logger.info(f"LocatorService processing image using {self.provider.__class__.__name__}")
        return self.provider.locate(image, context)

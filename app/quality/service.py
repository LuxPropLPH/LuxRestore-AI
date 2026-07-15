from app.interfaces.quality import BaseQualityEvaluator
from app.schemas.pipeline import QualityResult, ImageData, ExecutionContext
import logging

logger = logging.getLogger(__name__)

class QualityService:
    def __init__(self, provider: BaseQualityEvaluator):
        self.provider = provider

    def process(self, image: ImageData, context: ExecutionContext) -> QualityResult:
        logger.info(f"QualityService evaluating image using {self.provider.__class__.__name__}")
        return self.provider.evaluate(image, context)

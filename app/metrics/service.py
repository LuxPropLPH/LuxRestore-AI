from app.metrics.interfaces import BaseMetricsCalculator
from app.schemas.pipeline import ImageData, ExecutionContext
from app.metrics.schemas import MetricsResult
import logging

logger = logging.getLogger(__name__)

class MetricsService:
    def __init__(self, provider: BaseMetricsCalculator):
        self.provider = provider
        
    def process(self, original: ImageData, processed: ImageData, context: ExecutionContext) -> MetricsResult:
        logger.info(f"Calculating metrics using {self.provider.__class__.__name__}")
        return self.provider.calculate(original, processed, context)

from app.interfaces.mask import BaseMaskGenerator, BaseMaskRefiner
from app.schemas.pipeline import DetectionResult, MaskResult, ImageData, ExecutionContext
import logging

logger = logging.getLogger(__name__)

class MaskService:
    def __init__(self, generator: BaseMaskGenerator, refiner: BaseMaskRefiner):
        self.generator = generator
        self.refiner = refiner

    def process(self, image: ImageData, detections: DetectionResult, context: ExecutionContext) -> MaskResult:
        logger.info(f"MaskService generating mask using {self.generator.__class__.__name__}")
        mask = self.generator.generate(image, detections, context)
        
        logger.info(f"MaskService refining mask using {self.refiner.__class__.__name__}")
        refined_mask = self.refiner.refine(mask, context)
        return refined_mask

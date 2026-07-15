from app.preprocessing.interfaces import BaseLoader, BaseValidator, BaseNormalizer
from app.preprocessing.schemas import ImageSource
from app.schemas.pipeline import ImageData, ExecutionContext
import logging

logger = logging.getLogger(__name__)

class PreprocessingService:
    def __init__(self, loader: BaseLoader, validator: BaseValidator, normalizer: BaseNormalizer):
        self.loader = loader
        self.validator = validator
        self.normalizer = normalizer
        
    def process(self, source: ImageSource, context: ExecutionContext) -> ImageData:
        logger.info("Loading image...")
        raw_data = self.loader.load(source, context)
        
        logger.info("Validating image...")
        if not self.validator.validate(raw_data, context):
            raise ValueError("Image validation failed.")
            
        logger.info("Normalizing image...")
        return self.normalizer.normalize(raw_data, context)

from app.interfaces.inpainter import BaseInpainter
from app.schemas.pipeline import MaskResult, InpaintResult, ImageData, ExecutionContext
import logging

logger = logging.getLogger(__name__)

class InpainterService:
    def __init__(self, provider: BaseInpainter):
        self.provider = provider

    def process(self, image: ImageData, mask: MaskResult, context: ExecutionContext) -> InpaintResult:
        logger.info(f"InpainterService processing image using {self.provider.__class__.__name__}")
        return self.provider.inpaint(image, mask, context)

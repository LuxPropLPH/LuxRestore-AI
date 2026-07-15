from app.interfaces.mask import BaseMaskGenerator, BaseMaskRefiner
from app.schemas.pipeline import DetectionResult, MaskResult, ImageData, ExecutionContext

class MockMaskGenerator(BaseMaskGenerator):
    def generate(self, image: ImageData, detections: DetectionResult, context: ExecutionContext) -> MaskResult:
        return MaskResult(mask_data="dummy_mask_data", confidence=0.95)

class MockMaskRefiner(BaseMaskRefiner):
    def refine(self, mask: MaskResult, context: ExecutionContext) -> MaskResult:
        return MaskResult(mask_data="refined_dummy_mask_data", confidence=0.98)

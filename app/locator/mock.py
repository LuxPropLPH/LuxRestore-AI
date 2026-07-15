import uuid
from app.interfaces.locator import BaseLocator
from app.schemas.pipeline import DetectionResult, BoundingBox, RegionOfInterest, ImageData, ExecutionContext
from app.schemas.enums import DetectionType
from app.schemas.provider import ProviderMetadata, ProviderCapabilities

class MockLocator(BaseLocator):
    @classmethod
    def get_metadata(cls) -> ProviderMetadata:
        return ProviderMetadata(
            name="MockLocator",
            version="1.0.0",
            description="Mock locator provider for testing pipeline orchestration.",
            capabilities=ProviderCapabilities(
                supports_cpu=True,
                supports_gpu=False,
                supports_batch=True,
                returns_bounding_boxes=True,
                returns_masks=False
            ),
            model_info=None
        )

    def self_test(self) -> bool:
        return True

    def locate(self, image: ImageData, context: ExecutionContext) -> DetectionResult:
        dummy_box = BoundingBox(
            x1=10, y1=10, x2=100, y2=100,
            confidence=0.99,
            label=DetectionType.WATERMARK
        )
        dummy_region = RegionOfInterest(
            id=str(uuid.uuid4()),
            label=DetectionType.WATERMARK,
            confidence=0.99,
            bbox=dummy_box,
            metadata={"mocked": True, "request_id": context.request_id}
        )
        return DetectionResult(regions=[dummy_region])

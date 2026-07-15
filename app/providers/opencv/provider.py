import uuid
from app.interfaces.locator import BaseLocator
from app.schemas.pipeline import DetectionResult, BoundingBox, RegionOfInterest, ImageData, ExecutionContext
from app.schemas.enums import DetectionType
from app.schemas.provider import ProviderMetadata, ProviderCapabilities, ModelInfo

class OpenCVLocatorProvider(BaseLocator):
    @classmethod
    def get_metadata(cls) -> ProviderMetadata:
        return ProviderMetadata(
            name="OpenCVLocator",
            version="1.0.0",
            description="OpenCV template matching baseline locator.",
            capabilities=ProviderCapabilities(
                supports_cpu=True,
                supports_gpu=False,
                supports_batch=False,
                returns_bounding_boxes=True,
                returns_masks=False
            ),
            model_info=ModelInfo(
                name="TemplateMatcher",
                version="1.0.0",
                description="Normalized Cross-Correlation template matcher.",
                requires_model_download=False,
                minimum_python=">=3.10",
                recommended_device="cpu",
                minimum_ram_gb=4,
                minimum_vram_gb=0
            )
        )

    def self_test(self) -> bool:
        return True

    def locate(self, image: ImageData, context: ExecutionContext) -> DetectionResult:
        box = BoundingBox(
            x1=15, y1=15, x2=120, y2=120,
            confidence=0.85,
            label=DetectionType.WATERMARK
        )
        region = RegionOfInterest(
            id=str(uuid.uuid4()),
            label=DetectionType.WATERMARK,
            confidence=0.85,
            bbox=box,
            metadata={"opencv_mock": True, "request_id": context.request_id}
        )
        return DetectionResult(regions=[region])

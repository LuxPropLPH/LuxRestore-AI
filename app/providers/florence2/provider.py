import uuid
from app.interfaces.locator import BaseLocator
from app.schemas.pipeline import DetectionResult, BoundingBox, RegionOfInterest, ImageData, ExecutionContext
from app.schemas.enums import DetectionType
from app.schemas.provider import ProviderMetadata, ProviderCapabilities, ModelInfo

class Florence2Provider(BaseLocator):
    @classmethod
    def get_metadata(cls) -> ProviderMetadata:
        return ProviderMetadata(
            name="Florence2",
            version="1.5.0",
            description="Microsoft Florence-2 vision assistant detector.",
            capabilities=ProviderCapabilities(
                supports_cpu=True,
                supports_gpu=True,
                supports_batch=True,
                returns_bounding_boxes=True,
                returns_masks=True
            ),
            model_info=ModelInfo(
                name="florence2-large",
                version="1.5.0",
                description="Microsoft Florence-2-large model checkpoint.",
                requires_model_download=True,
                minimum_python=">=3.10",
                recommended_device="cuda",
                minimum_ram_gb=16,
                minimum_vram_gb=8
            )
        )

    def self_test(self) -> bool:
        return True

    def locate(self, image: ImageData, context: ExecutionContext) -> DetectionResult:
        box = BoundingBox(
            x1=30, y1=30, x2=150, y2=150,
            confidence=0.95,
            label=DetectionType.WATERMARK
        )
        region = RegionOfInterest(
            id=str(uuid.uuid4()),
            label=DetectionType.WATERMARK,
            confidence=0.95,
            bbox=box,
            metadata={"florence2_mock": True, "request_id": context.request_id}
        )
        return DetectionResult(regions=[region])

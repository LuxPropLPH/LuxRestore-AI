import uuid
from app.interfaces.locator import BaseLocator
from app.schemas.pipeline import DetectionResult, BoundingBox, RegionOfInterest, ImageData, ExecutionContext
from app.schemas.enums import DetectionType
from app.schemas.provider import ProviderMetadata, ProviderCapabilities, ModelInfo

class GroundingDINOProvider(BaseLocator):
    @classmethod
    def get_metadata(cls) -> ProviderMetadata:
        return ProviderMetadata(
            name="GroundingDINO",
            version="2.0.0",
            description="GroundingDINO open-set object detector.",
            capabilities=ProviderCapabilities(
                supports_cpu=True,
                supports_gpu=True,
                supports_batch=True,
                returns_bounding_boxes=True,
                returns_masks=False
            ),
            model_info=ModelInfo(
                name="groundingdino-swint-ogc",
                version="2.0.0",
                description="GroundingDINO Swin-T OGC weights.",
                requires_model_download=True,
                minimum_python=">=3.10",
                recommended_device="cuda",
                minimum_ram_gb=16,
                minimum_vram_gb=6
            )
        )

    def self_test(self) -> bool:
        return True

    def locate(self, image: ImageData, context: ExecutionContext) -> DetectionResult:
        box = BoundingBox(
            x1=50, y1=50, x2=200, y2=200,
            confidence=0.92,
            label=DetectionType.WATERMARK
        )
        region = RegionOfInterest(
            id=str(uuid.uuid4()),
            label=DetectionType.WATERMARK,
            confidence=0.92,
            bbox=box,
            metadata={"grounding_dino_mock": True, "request_id": context.request_id}
        )
        return DetectionResult(regions=[region])

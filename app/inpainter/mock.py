import uuid
from app.interfaces.inpainter import BaseInpainter
from app.schemas.pipeline import MaskResult, InpaintResult, ImageData, ExecutionContext

class MockInpainter(BaseInpainter):
    def inpaint(self, image: ImageData, mask: MaskResult, context: ExecutionContext) -> InpaintResult:
        dummy_image = ImageData(
            id=str(uuid.uuid4()),
            source="mock_inpainter",
            width=image.width,
            height=image.height,
            channels=image.channels,
            format=image.format,
            metadata={"mocked_inpainted": True, "request_id": context.request_id},
            image="dummy_inpainted_image_data"
        )
        return InpaintResult(image_data=dummy_image)

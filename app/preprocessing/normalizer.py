import uuid
from typing import Any
from app.preprocessing.interfaces import BaseNormalizer
from app.schemas.pipeline import ImageData, ExecutionContext

class MockNormalizer(BaseNormalizer):
    def normalize(self, image: Any, context: ExecutionContext) -> ImageData:
        return ImageData(
            id=str(uuid.uuid4()),
            source="mock_normalizer",
            width=1024,
            height=1024,
            channels=3,
            format="RGB",
            image=image
        )

from typing import Any
from app.preprocessing.interfaces import BaseLoader
from app.preprocessing.schemas import ImageSource
from app.schemas.pipeline import ExecutionContext

class MockLoader(BaseLoader):
    def load(self, source: ImageSource, context: ExecutionContext) -> Any:
        return b"mocked_raw_image_data"

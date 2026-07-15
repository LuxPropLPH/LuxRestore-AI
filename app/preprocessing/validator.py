from typing import Any
from app.preprocessing.interfaces import BaseValidator
from app.schemas.pipeline import ExecutionContext

class MockValidator(BaseValidator):
    def validate(self, image: Any, context: ExecutionContext) -> bool:
        return True

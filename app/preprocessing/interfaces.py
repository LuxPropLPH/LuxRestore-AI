from abc import ABC, abstractmethod
from typing import Any
from app.schemas.pipeline import ImageData, ExecutionContext
from app.preprocessing.schemas import ImageSource

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: ImageSource, context: ExecutionContext) -> Any:
        pass

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, image: Any, context: ExecutionContext) -> bool:
        pass

class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(self, image: Any, context: ExecutionContext) -> ImageData:
        pass

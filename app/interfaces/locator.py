from abc import ABC, abstractmethod
from app.schemas.pipeline import DetectionResult, ImageData, ExecutionContext
from app.schemas.provider import ProviderMetadata, ProviderCapabilities

class BaseLocator(ABC):
    @classmethod
    @abstractmethod
    def get_metadata(cls) -> ProviderMetadata:
        pass

    def metadata(self) -> ProviderMetadata:
        return self.get_metadata()

    def capabilities(self) -> ProviderCapabilities:
        return self.metadata().capabilities

    @abstractmethod
    def self_test(self) -> bool:
        pass

    @abstractmethod
    def locate(self, image: ImageData, context: ExecutionContext) -> DetectionResult:
        pass

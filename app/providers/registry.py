from typing import Dict, Type, List
from app.interfaces.locator import BaseLocator
from app.schemas.enums import ProviderType
from app.schemas.provider import ProviderMetadata

class ProviderRegistry:
    def __init__(self):
        self._registry: Dict[ProviderType, Type[BaseLocator]] = {}

    def register(self, provider_type: ProviderType, cls: Type[BaseLocator]) -> None:
        self._registry[provider_type] = cls

    def get(self, provider_type: ProviderType) -> BaseLocator:
        cls = self._registry.get(provider_type)
        if not cls:
            raise NotImplementedError(f"Provider {provider_type} is not implemented or registered.")
        return cls()

    def list_providers(self) -> List[ProviderMetadata]:
        return [cls.get_metadata() for cls in self._registry.values()]

default_registry = ProviderRegistry()

# Lazy imports to avoid circular dependencies
from app.locator.mock import MockLocator
from app.providers.opencv.provider import OpenCVLocatorProvider
from app.providers.grounding_dino.provider import GroundingDINOProvider
from app.providers.florence2.provider import Florence2Provider

default_registry.register(ProviderType.MOCK, MockLocator)
default_registry.register(ProviderType.OPENCV, OpenCVLocatorProvider)
default_registry.register(ProviderType.GROUNDING_DINO, GroundingDINOProvider)
default_registry.register(ProviderType.FLORENCE2, Florence2Provider)

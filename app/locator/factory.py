from app.interfaces.locator import BaseLocator
from app.schemas.enums import ProviderType
from app.providers.registry import default_registry

class LocatorFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseLocator:
        return default_registry.get(provider_type)

from app.interfaces.inpainter import BaseInpainter
from app.schemas.enums import ProviderType
from app.inpainter.mock import MockInpainter

class InpainterFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseInpainter:
        if provider_type == ProviderType.MOCK:
            return MockInpainter()
        raise NotImplementedError(f"Inpainter provider {provider_type} is not implemented yet.")

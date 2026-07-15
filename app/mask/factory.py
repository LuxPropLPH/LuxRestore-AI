from app.interfaces.mask import BaseMaskGenerator, BaseMaskRefiner
from app.schemas.enums import ProviderType
from app.mask.mock import MockMaskGenerator, MockMaskRefiner

class MaskGeneratorFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseMaskGenerator:
        if provider_type == ProviderType.MOCK:
            return MockMaskGenerator()
        raise NotImplementedError(f"Mask generator provider {provider_type} is not implemented yet.")

class MaskRefinerFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseMaskRefiner:
        if provider_type == ProviderType.MOCK:
            return MockMaskRefiner()
        raise NotImplementedError(f"Mask refiner provider {provider_type} is not implemented yet.")

from app.interfaces.quality import BaseQualityEvaluator
from app.schemas.enums import ProviderType
from app.quality.mock import MockQualityEvaluator

class QualityFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseQualityEvaluator:
        if provider_type == ProviderType.MOCK:
            return MockQualityEvaluator()
        raise NotImplementedError(f"Quality provider {provider_type} is not implemented yet.")

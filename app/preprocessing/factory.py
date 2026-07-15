from app.preprocessing.interfaces import BaseLoader, BaseValidator, BaseNormalizer
from app.preprocessing.loader import MockLoader
from app.preprocessing.validator import MockValidator
from app.preprocessing.normalizer import MockNormalizer
from app.schemas.enums import ProviderType

class PreprocessingFactory:
    @staticmethod
    def get_loader(provider_type: ProviderType) -> BaseLoader:
        if provider_type == ProviderType.MOCK:
            return MockLoader()
        raise NotImplementedError()
        
    @staticmethod
    def get_validator(provider_type: ProviderType) -> BaseValidator:
        if provider_type == ProviderType.MOCK:
            return MockValidator()
        raise NotImplementedError()
        
    @staticmethod
    def get_normalizer(provider_type: ProviderType) -> BaseNormalizer:
        if provider_type == ProviderType.MOCK:
            return MockNormalizer()
        raise NotImplementedError()

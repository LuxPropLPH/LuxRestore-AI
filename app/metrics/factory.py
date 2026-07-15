from app.metrics.interfaces import BaseMetricsCalculator
from app.schemas.enums import ProviderType
from app.metrics.metrics import MockMetricsCalculator

class MetricsFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseMetricsCalculator:
        if provider_type == ProviderType.MOCK:
            return MockMetricsCalculator()
        raise NotImplementedError()

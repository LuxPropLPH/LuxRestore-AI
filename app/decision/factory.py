from app.decision.interfaces import BaseDecisionEngine
from app.schemas.enums import ProviderType
from app.decision.engine import MockDecisionEngine

class DecisionFactory:
    @staticmethod
    def get_provider(provider_type: ProviderType) -> BaseDecisionEngine:
        if provider_type == ProviderType.MOCK:
            return MockDecisionEngine()
        raise NotImplementedError()

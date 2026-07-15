from app.decision.interfaces import BaseDecisionEngine
from app.schemas.pipeline import PipelineState, ExecutionContext

class MockDecisionEngine(BaseDecisionEngine):
    def decide(self, state: PipelineState, context: ExecutionContext) -> str:
        return "PROCEED_DEFAULT"

from abc import ABC, abstractmethod
from app.schemas.pipeline import PipelineState, ExecutionContext

class BaseDecisionEngine(ABC):
    @abstractmethod
    def decide(self, state: PipelineState, context: ExecutionContext) -> str:
        """
        Decides on the routing or parameters based on current state.
        For now, returns a simple string representing the action.
        """
        pass

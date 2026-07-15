from app.decision.interfaces import BaseDecisionEngine
from app.schemas.pipeline import PipelineState, ExecutionContext
import logging

logger = logging.getLogger(__name__)

class DecisionService:
    def __init__(self, engine: BaseDecisionEngine):
        self.engine = engine
        
    def process(self, state: PipelineState, context: ExecutionContext) -> str:
        logger.info(f"Making decision using {self.engine.__class__.__name__}")
        return self.engine.decide(state, context)

from app.interfaces.quality import BaseQualityEvaluator
from app.schemas.pipeline import QualityResult, ImageData, ExecutionContext

class MockQualityEvaluator(BaseQualityEvaluator):
    def evaluate(self, image: ImageData, context: ExecutionContext) -> QualityResult:
        return QualityResult(score=0.98, passed=True, feedback="Looks great")

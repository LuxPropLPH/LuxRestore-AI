from app.metrics.interfaces import BaseMetricsCalculator
from app.schemas.pipeline import ImageData, ExecutionContext
from app.metrics.schemas import MetricsResult

class MockMetricsCalculator(BaseMetricsCalculator):
    def calculate(self, original: ImageData, processed: ImageData, context: ExecutionContext) -> MetricsResult:
        return MetricsResult(
            lpips=0.05,
            ssim=0.95,
            psnr=32.5,
            runtime_ms=120.0,
            gpu_memory_mb=512.0
        )

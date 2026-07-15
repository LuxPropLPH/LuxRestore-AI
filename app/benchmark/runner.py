import time
import traceback
from typing import List
from app.benchmark.schemas import BenchmarkResult
from app.schemas.pipeline import ImageData, ExecutionContext
from app.schemas.enums import ProviderType
from app.providers.registry import default_registry

class BenchmarkRunner:
    def __init__(self, provider_types: List[ProviderType]):
        self.provider_types = provider_types

    def run(self, image: ImageData, context: ExecutionContext) -> List[BenchmarkResult]:
        results = []
        for p_type in self.provider_types:
            try:
                provider = default_registry.get(p_type)
                provider.self_test()
                
                t0 = time.time()
                provider.locate(image, context)
                elapsed_ms = (time.time() - t0) * 1000.0

                results.append(BenchmarkResult(
                    provider_name=provider.metadata().name,
                    execution_time_ms=elapsed_ms,
                    success=True,
                    notes=f"Successfully executed mock detection for {p_type.value}."
                ))
            except Exception as e:
                results.append(BenchmarkResult(
                    provider_name=p_type.value,
                    execution_time_ms=0.0,
                    success=False,
                    notes=f"Failed to execute provider: {str(e)}",
                    exception=traceback.format_exc()
                ))
        return results

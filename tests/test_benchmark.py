import uuid
from app.benchmark.runner import BenchmarkRunner
from app.schemas.enums import ProviderType
from app.schemas.pipeline import ImageData, ExecutionContext

def test_benchmark_runner_success():
    runner = BenchmarkRunner(provider_types=[
        ProviderType.MOCK,
        ProviderType.OPENCV,
        ProviderType.GROUNDING_DINO,
        ProviderType.FLORENCE2
    ])
    
    image = ImageData(
        id="bench-image-1",
        source="test",
        width=512,
        height=512,
        channels=3,
        format="RGB"
    )
    context = ExecutionContext(request_id=str(uuid.uuid4()))
    
    results = runner.run(image, context)
    assert len(results) == 4
    for result in results:
        assert result.success is True
        assert result.execution_time_ms >= 0.0
        assert result.exception is None
        assert result.notes != ""

def test_benchmark_runner_exception_handling():
    runner = BenchmarkRunner(provider_types=[ProviderType.YOLO])
    image = ImageData(
        id="bench-image-2",
        source="test",
        width=512,
        height=512,
        channels=3,
        format="RGB"
    )
    context = ExecutionContext(request_id=str(uuid.uuid4()))
    
    results = runner.run(image, context)
    assert len(results) == 1
    assert results[0].success is False
    assert results[0].exception is not None
    assert "NotImplementedError" in results[0].exception

from app.schemas.enums import ProviderType
from app.preprocessing.schemas import ImageSource
from app.preprocessing.factory import PreprocessingFactory
from app.preprocessing.service import PreprocessingService
from app.locator.factory import LocatorFactory
from app.locator.service import LocatorService
from app.mask.factory import MaskGeneratorFactory, MaskRefinerFactory
from app.mask.service import MaskService
from app.decision.factory import DecisionFactory
from app.decision.service import DecisionService
from app.inpainter.factory import InpainterFactory
from app.inpainter.service import InpainterService
from app.metrics.factory import MetricsFactory
from app.metrics.service import MetricsService
from app.quality.factory import QualityFactory
from app.quality.service import QualityService
from app.pipeline.orchestrator import PipelineOrchestrator


def _build_orchestrator() -> PipelineOrchestrator:
    provider = ProviderType.MOCK

    preprocessing = PreprocessingService(
        loader=PreprocessingFactory.get_loader(provider),
        validator=PreprocessingFactory.get_validator(provider),
        normalizer=PreprocessingFactory.get_normalizer(provider),
    )
    locator = LocatorService(LocatorFactory.get_provider(provider))
    mask = MaskService(
        generator=MaskGeneratorFactory.get_provider(provider),
        refiner=MaskRefinerFactory.get_provider(provider),
    )
    decision = DecisionService(DecisionFactory.get_provider(provider))
    inpainter = InpainterService(InpainterFactory.get_provider(provider))
    metrics = MetricsService(MetricsFactory.get_provider(provider))
    quality = QualityService(QualityFactory.get_provider(provider))

    return PipelineOrchestrator(
        preprocessing=preprocessing,
        locator=locator,
        mask_generator=mask,
        decision_engine=decision,
        inpainter=inpainter,
        metrics=metrics,
        quality=quality,
    )


def test_pipeline_full_run():
    orchestrator = _build_orchestrator()
    source = ImageSource(data="test_image.png", is_path=True)

    result = orchestrator.run(source, request_id="test-req-001")

    assert result.success is True
    assert result.error_message == ""
    assert "request_id" in result.metadata
    assert result.metadata["request_id"] == "test-req-001"
    assert "timings" in result.metadata
    assert "metrics" in result.metadata


def test_pipeline_result_contains_timings():
    orchestrator = _build_orchestrator()
    source = ImageSource(data="test_image.png", is_path=True)

    result = orchestrator.run(source)

    timings = result.metadata["timings"]
    expected_stages = [
        "preprocessing", "locator", "mask_generation",
        "decision", "inpainter", "metrics", "quality",
    ]
    for stage in expected_stages:
        assert stage in timings, f"Missing timing for stage: {stage}"


def test_pipeline_result_contains_metrics():
    orchestrator = _build_orchestrator()
    source = ImageSource(data="test_image.png", is_path=True)

    result = orchestrator.run(source)

    metrics = result.metadata["metrics"]
    assert "lpips" in metrics
    assert "ssim" in metrics
    assert "psnr" in metrics
    assert "runtime_ms" in metrics
    assert "gpu_memory_mb" in metrics


def test_pipeline_result_contains_quality():
    orchestrator = _build_orchestrator()
    source = ImageSource(data="test_image.png", is_path=True)

    result = orchestrator.run(source)

    assert "quality_score" in result.metadata
    assert result.metadata["quality_score"] == 0.98
    assert result.metadata["quality_feedback"] == "Looks great"

from app.schemas.enums import DetectionType, ProviderType
from app.schemas.pipeline import (
    BoundingBox, 
    DetectionResult, 
    ImageData, 
    RegionOfInterest, 
    ExecutionContext, 
    PipelineState, 
    PipelineResult
)


def test_enums():
    assert DetectionType.WATERMARK == "WATERMARK"
    assert ProviderType.MOCK == "MOCK"


def test_bounding_box():
    box = BoundingBox(x1=0, y1=0, x2=10, y2=10, confidence=0.9, label=DetectionType.LOGO)
    assert box.x1 == 0
    assert box.label == DetectionType.LOGO


def test_detection_result_defaults_empty():
    res = DetectionResult()
    assert len(res.regions) == 0


def test_image_data():
    img = ImageData(
        id="test-1",
        source="unit_test",
        width=512,
        height=512,
        channels=3,
        format="RGB",
    )
    assert img.image is None
    assert img.width == 512


def test_image_data_with_arbitrary_image():
    """image field accepts any type — PIL, numpy, tensor, bytes."""
    img = ImageData(
        id="test-2",
        source="unit_test",
        width=256,
        height=256,
        channels=3,
        format="RGB",
        image=b"raw_bytes",
    )
    assert img.image == b"raw_bytes"


def test_region_of_interest():
    box = BoundingBox(x1=5, y1=5, x2=50, y2=50, confidence=0.95, label=DetectionType.WATERMARK)
    roi = RegionOfInterest(
        id="roi-1",
        label=DetectionType.WATERMARK,
        confidence=0.95,
        bbox=box,
        metadata={"source": "test"},
    )
    assert roi.bbox.x1 == 5
    assert roi.metadata["source"] == "test"


def test_execution_context_defaults():
    ctx = ExecutionContext(request_id="req-1")
    assert ctx.device == "cpu"
    assert ctx.debug is False
    assert ctx.provider == "MOCK"
    assert ctx.timings == {}


def test_pipeline_state_defaults():
    state = PipelineState()
    assert state.original_image is None
    assert state.regions is None
    assert state.timings == {}


def test_pipeline_result_defaults():
    result = PipelineResult()
    assert result.success is False
    assert result.warnings == []
    assert result.final_image is None

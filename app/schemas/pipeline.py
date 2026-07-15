from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from app.schemas.enums import DetectionType

class ImageData(BaseModel):
    id: str
    source: str
    width: int
    height: int
    channels: int
    format: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    image: Optional[Any] = None

class ExecutionContext(BaseModel):
    request_id: str
    device: str = "cpu"
    batch_id: Optional[str] = None
    timings: Dict[str, float] = Field(default_factory=dict)
    debug: bool = False
    provider: str = "MOCK"
    settings: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float
    label: DetectionType

class RegionOfInterest(BaseModel):
    id: str
    label: DetectionType
    confidence: float
    bbox: BoundingBox
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DetectionResult(BaseModel):
    regions: List[RegionOfInterest] = Field(default_factory=list)

class MaskResult(BaseModel):
    mask_data: Any
    confidence: float = 1.0

class InpaintResult(BaseModel):
    image_data: ImageData

class QualityResult(BaseModel):
    score: float
    passed: bool
    feedback: str = ""

class PipelineState(BaseModel):
    original_image: Optional[ImageData] = None
    regions: Optional[DetectionResult] = None
    mask: Optional[MaskResult] = None
    inpainted: Optional[InpaintResult] = None
    quality: Optional[QualityResult] = None
    timings: Dict[str, float] = Field(default_factory=dict)
    provider_info: Dict[str, str] = Field(default_factory=dict)

class PipelineResult(BaseModel):
    final_image: Optional[Any] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    success: bool = False
    warnings: List[str] = Field(default_factory=list)
    error_message: str = ""

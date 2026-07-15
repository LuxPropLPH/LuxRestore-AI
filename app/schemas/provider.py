from pydantic import BaseModel
from typing import Optional

class ProviderCapabilities(BaseModel):
    supports_batch: bool
    supports_cpu: bool
    supports_gpu: bool
    returns_bounding_boxes: bool
    returns_masks: bool

class ModelInfo(BaseModel):
    name: str
    version: str
    description: str
    requires_model_download: bool
    minimum_python: str
    recommended_device: str
    minimum_ram_gb: int
    minimum_vram_gb: int

class ProviderMetadata(BaseModel):
    name: str
    version: str
    description: str
    capabilities: ProviderCapabilities
    model_info: Optional[ModelInfo] = None

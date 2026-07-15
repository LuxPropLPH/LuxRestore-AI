from pydantic import BaseModel

class MetricsResult(BaseModel):
    lpips: float
    ssim: float
    psnr: float
    runtime_ms: float
    gpu_memory_mb: float

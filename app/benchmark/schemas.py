from pydantic import BaseModel
from typing import Optional

class BenchmarkResult(BaseModel):
    provider_name: str
    execution_time_ms: float
    success: bool
    notes: str
    exception: Optional[str] = None

from pydantic_settings import BaseSettings
from app.schemas.enums import ProviderType
from typing import Dict

class Settings(BaseSettings):
    project_name: str = "LuxRestore-AI"
    version: str = "0.1.0"
    
    locator_provider: ProviderType = ProviderType.MOCK
    segmenter_provider: ProviderType = ProviderType.MOCK
    inpainter_provider: ProviderType = ProviderType.MOCK
    quality_provider: ProviderType = ProviderType.MOCK
    
    future_model_paths: Dict[str, str] = {}
    batch_size: int = 1
    device: str = "cpu"

    class Config:
        env_file = ".env"

settings = Settings()

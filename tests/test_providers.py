import pytest
from app.schemas.enums import ProviderType
from app.providers.registry import default_registry

def test_provider_metadata_and_model_info():
    for provider_type in [ProviderType.MOCK, ProviderType.OPENCV, ProviderType.GROUNDING_DINO, ProviderType.FLORENCE2]:
        provider = default_registry.get(provider_type)
        metadata = provider.metadata()
        assert metadata.name is not None
        assert metadata.version is not None
        assert metadata.description is not None
        
        caps = metadata.capabilities
        assert caps.supports_cpu is True or caps.supports_cpu is False
        assert caps.supports_gpu is True or caps.supports_gpu is False
        
        if provider_type == ProviderType.FLORENCE2:
            assert metadata.model_info is not None
            assert metadata.model_info.name == "florence2-large"
            assert metadata.model_info.minimum_python == ">=3.10"
            assert metadata.model_info.recommended_device == "cuda"
            assert metadata.model_info.minimum_ram_gb == 16
            assert metadata.model_info.minimum_vram_gb == 8

def test_provider_self_test():
    for provider_type in [ProviderType.MOCK, ProviderType.OPENCV, ProviderType.GROUNDING_DINO, ProviderType.FLORENCE2]:
        provider = default_registry.get(provider_type)
        assert provider.self_test() is True

def test_registry_metadata():
    providers_meta = default_registry.list_providers()
    assert len(providers_meta) == 4
    names = [meta.name for meta in providers_meta]
    assert "MockLocator" in names
    assert "OpenCVLocator" in names
    assert "GroundingDINO" in names
    assert "Florence2" in names

import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException
from app.preprocessing.schemas import ImageSource
from app.preprocessing.service import PreprocessingService
from app.preprocessing.factory import PreprocessingFactory
from app.locator.factory import LocatorFactory
from app.schemas.pipeline import DetectionResult, ExecutionContext
from app.schemas.enums import ProviderType
from app.config.settings import settings

router = APIRouter()

preprocessing = PreprocessingService(
    loader=PreprocessingFactory.get_loader(ProviderType.MOCK),
    validator=PreprocessingFactory.get_validator(ProviderType.MOCK),
    normalizer=PreprocessingFactory.get_normalizer(ProviderType.MOCK),
)

@router.post("/locate", response_model=DetectionResult, summary="Development/Debug Bounding Box Locator")
def locate_objects(source: ImageSource, provider: Optional[ProviderType] = None) -> DetectionResult:
    """
    Development/Debug Endpoint to run the configured or overridden locator provider on a single image.
    This is not intended to be used as the production restoration API.
    Future production restoration should be accessed via POST /restore (not implemented).
    """
    try:
        selected_provider = provider or settings.locator_provider
        context = ExecutionContext(
            request_id=str(uuid.uuid4()),
            provider=selected_provider.value,
            settings={"locator_provider": selected_provider}
        )
        image_data = preprocessing.process(source, context)
        locator = LocatorFactory.get_provider(selected_provider)
        return locator.locate(image_data, context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

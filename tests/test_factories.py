import pytest
from app.schemas.enums import ProviderType

from app.locator.factory import LocatorFactory
from app.locator.mock import MockLocator

from app.mask.factory import MaskGeneratorFactory, MaskRefinerFactory
from app.mask.mock import MockMaskGenerator, MockMaskRefiner

from app.inpainter.factory import InpainterFactory
from app.inpainter.mock import MockInpainter

from app.quality.factory import QualityFactory
from app.quality.mock import MockQualityEvaluator

from app.preprocessing.factory import PreprocessingFactory
from app.preprocessing.loader import MockLoader
from app.preprocessing.validator import MockValidator
from app.preprocessing.normalizer import MockNormalizer

from app.metrics.factory import MetricsFactory
from app.metrics.metrics import MockMetricsCalculator

from app.decision.factory import DecisionFactory
from app.decision.engine import MockDecisionEngine


def test_locator_factory_mock():
    provider = LocatorFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockLocator)


def test_locator_factory_unimplemented():
    with pytest.raises(NotImplementedError):
        LocatorFactory.get_provider(ProviderType.YOLO)


def test_mask_generator_factory_mock():
    provider = MaskGeneratorFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockMaskGenerator)


def test_mask_refiner_factory_mock():
    provider = MaskRefinerFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockMaskRefiner)


def test_inpainter_factory_mock():
    provider = InpainterFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockInpainter)


def test_quality_factory_mock():
    provider = QualityFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockQualityEvaluator)


def test_preprocessing_factory_mock():
    loader = PreprocessingFactory.get_loader(ProviderType.MOCK)
    validator = PreprocessingFactory.get_validator(ProviderType.MOCK)
    normalizer = PreprocessingFactory.get_normalizer(ProviderType.MOCK)
    assert isinstance(loader, MockLoader)
    assert isinstance(validator, MockValidator)
    assert isinstance(normalizer, MockNormalizer)


def test_metrics_factory_mock():
    provider = MetricsFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockMetricsCalculator)


def test_decision_factory_mock():
    provider = DecisionFactory.get_provider(ProviderType.MOCK)
    assert isinstance(provider, MockDecisionEngine)

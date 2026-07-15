import uuid
import time
from typing import Dict, Any, Optional
import logging

from app.schemas.pipeline import (
    ImageData, 
    DetectionResult, 
    MaskResult, 
    InpaintResult, 
    QualityResult, 
    PipelineResult, 
    PipelineState, 
    ExecutionContext
)
from app.preprocessing.schemas import ImageSource

from app.preprocessing.service import PreprocessingService
from app.locator.service import LocatorService
from app.mask.service import MaskService
from app.decision.service import DecisionService
from app.inpainter.service import InpainterService
from app.metrics.service import MetricsService
from app.quality.service import QualityService

logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    def __init__(
        self,
        preprocessing: PreprocessingService,
        locator: LocatorService,
        mask_generator: MaskService,
        decision_engine: DecisionService,
        inpainter: InpainterService,
        metrics: MetricsService,
        quality: QualityService,
    ):
        self.preprocessing = preprocessing
        self.locator = locator
        self.mask_generator = mask_generator
        self.decision_engine = decision_engine
        self.inpainter = inpainter
        self.metrics = metrics
        self.quality = quality

    def run(
        self, 
        source: ImageSource, 
        request_id: Optional[str] = None, 
        settings: Optional[Dict[str, Any]] = None
    ) -> PipelineResult:
        if not request_id:
            request_id = str(uuid.uuid4())
            
        context = ExecutionContext(
            request_id=request_id,
            settings=settings or {},
            timings={}
        )
        
        state = PipelineState()
        result = PipelineResult()

        start_total = time.time()
        
        try:
            # 1. Preprocessing
            t0 = time.time()
            state.original_image = self.preprocessing.process(source, context)
            context.timings["preprocessing"] = time.time() - t0

            # 2. Locator
            t0 = time.time()
            state.regions = self.locator.process(state.original_image, context)
            context.timings["locator"] = time.time() - t0

            # 3. Mask Generation & Refinement
            t0 = time.time()
            state.mask = self.mask_generator.process(state.original_image, state.regions, context)
            context.timings["mask_generation"] = time.time() - t0
            
            # 4. Decision Engine
            t0 = time.time()
            decision = self.decision_engine.process(state, context)
            context.timings["decision"] = time.time() - t0
            
            logger.info(f"Decision Engine recommended: {decision}")

            # 5. Inpainting
            t0 = time.time()
            state.inpainted = self.inpainter.process(state.original_image, state.mask, context)
            context.timings["inpainter"] = time.time() - t0

            # 6. Metrics
            t0 = time.time()
            metrics_result = self.metrics.process(state.original_image, state.inpainted.image_data, context)
            context.timings["metrics"] = time.time() - t0

            # 7. Quality Evaluation
            t0 = time.time()
            state.quality = self.quality.process(state.inpainted.image_data, context)
            context.timings["quality"] = time.time() - t0

            # Build final API result
            result.final_image = state.inpainted.image_data.image
            result.success = state.quality.passed
            result.metadata = {
                "request_id": context.request_id,
                "timings": context.timings,
                "metrics": metrics_result.model_dump(),
                "quality_score": state.quality.score,
                "quality_feedback": state.quality.feedback,
            }

            context.timings["total"] = time.time() - start_total
            state.timings = context.timings

            return result

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            result.success = False
            result.error_message = str(e)
            return result

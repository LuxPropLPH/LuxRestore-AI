from typing import Dict, Any, List
from PIL import Image
import logging

from playground.grounding_dino.adapter import GroundingDINOAdapter

logger = logging.getLogger("grounding_dino_playground.locator")

class GroundingDINOLocator:
    def __init__(self, adapter: GroundingDINOAdapter, model_path: str, device: str):
        self.adapter = adapter
        self.model_path = model_path
        self.device = device
        self.is_loaded = False

    def load_model(self) -> None:
        """Load the model via the adapter."""
        logger.info("Initializing GroundingDINO via Adapter...")
        self.adapter.load(self.model_path, self.device)
        self.is_loaded = True

    def locate(self, image: Image.Image, prompt: str, threshold: float) -> List[Dict[str, Any]]:
        """Run Zero-Shot Bounding Box detection."""
        if not self.is_loaded:
            self.load_model()
        return self.adapter.detect(image, prompt, threshold)

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from PIL import Image

class GroundingDINOAdapter(ABC):
    """Abstraction layer so the locator isn't tied directly to HF transformers."""
    
    @abstractmethod
    def load(self, model_path: str, device: str) -> None:
        """Initialize the model weights and config from the local path."""
        pass

    @abstractmethod
    def detect(self, image: Image.Image, prompt: str, threshold: float) -> List[Dict[str, Any]]:
        """Run object detection on the PIL image using the prompt and threshold."""
        pass

class HFTransformersAdapter(GroundingDINOAdapter):
    """Hugging Face Transformers implementation of GroundingDINO."""
    
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = "cpu"

    def load(self, model_path: str, device: str) -> None:
        import torch
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
        
        self.device = device
        self.processor = AutoProcessor.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_path, local_files_only=True)
        self.model.to(self.device)

    def detect(self, image: Image.Image, prompt: str, threshold: float) -> List[Dict[str, Any]]:
        import torch
        
        text_prompt = prompt if prompt.endswith(".") else f"{prompt}."
        inputs = self.processor(images=image, text=text_prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        results = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            box_threshold=threshold,
            text_threshold=threshold,
            target_sizes=[image.size[::-1]]
        )
        
        detections = []
        if len(results) > 0:
            result = results[0]
            boxes = result["boxes"].cpu().tolist()
            scores = result["scores"].cpu().tolist()
            labels = result["labels"]
            
            for box, score, label in zip(boxes, scores, labels):
                detections.append({
                    "box": [int(b) for b in box],
                    "score": round(score, 4),
                    "label": label
                })
        return detections

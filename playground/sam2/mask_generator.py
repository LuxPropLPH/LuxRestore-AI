import json
import time
from pathlib import Path
from typing import Any, Dict, List

from PIL import Image


class SAM2MaskGenerator:
    def __init__(self, adapter: Any, mask_threshold: float):
        self.adapter = adapter
        self.mask_threshold = mask_threshold

    def load_inputs(self, image_name: str, output_dir: Path) -> tuple[Image.Image, List[Dict[str, Any]]]:
        image_dir = output_dir / image_name
        original_path = image_dir / "original.jpg"
        detections_path = image_dir / "detections_final.json"
        if not detections_path.exists():
            detections_path = image_dir / "detections_merged.json"
        if not detections_path.exists():
            detections_path = image_dir / "detections.json"

        if not original_path.exists():
            raise FileNotFoundError(f"Missing GroundingDINO original image: {original_path}")
        if not detections_path.exists():
            raise FileNotFoundError(f"Missing GroundingDINO detections JSON: {detections_path}")

        image = Image.open(original_path).convert("RGB")
        detections = json.loads(detections_path.read_text(encoding="utf-8"))
        return image, detections

    def run(self, image_name: str, output_dir: Path) -> Dict[str, Any]:
        image, detections = self.load_inputs(image_name, output_dir)
        boxes = [self._box_to_prompt(detection["box"]) for detection in detections]

        start = time.time()
        if boxes:
            result = self.adapter.generate_masks(image, boxes, self.mask_threshold)
            masks = result["masks"]
        else:
            masks = []
        runtime_ms = (time.time() - start) * 1000.0

        return {
            "image": image,
            "detections": detections,
            "boxes": boxes,
            "masks": masks,
            "runtime_ms": runtime_ms,
        }

    def _box_to_prompt(self, box: List[float]) -> List[float]:
        return [float(box[0]), float(box[1]), float(box[2]), float(box[3])]

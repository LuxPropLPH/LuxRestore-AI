import json
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger("grounding_dino_playground.visualizer")

class ImageVisualizer:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def draw_detections(
        self,
        original_image: Image.Image,
        detections: List[Dict[str, Any]],
        prompt: str,
        filename: str
    ) -> None:
        """Draw bounding boxes and output original.jpg, detections.jpg, and detections.json."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = self.output_dir / f"{filename}_{prompt}_detections.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(detections, f, indent=4)
        logger.info(f"Saved detections JSON to {json_path}")
        
        orig_path = self.output_dir / f"{filename}_original.jpg"
        original_image.save(orig_path, "JPEG")
        
        draw_image = original_image.copy()
        draw = ImageDraw.Draw(draw_image)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
            
        for det in detections:
            box = det["box"]
            score = det["score"]
            label = det["label"]
            
            draw.rectangle(box, outline="red", width=3)
            text = f"{label}: {score:.2f} ({prompt})"
            draw.text((box[0] + 5, box[1] + 5), text, fill="red", font=font)

        det_path = self.output_dir / f"{filename}_{prompt}_detections.jpg"
        draw_image.save(det_path, "JPEG")
        logger.info(f"Saved detection visualization to {det_path}")

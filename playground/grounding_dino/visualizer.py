import json
from pathlib import Path
from typing import List, Dict, Any, Optional
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
        filename: str,
        runtime_ms: float,
        model_name: str,
        device: str,
        error: Optional[str] = None
    ) -> Path:
        """Create the per-image output folder and write validation artifacts."""
        image_dir = self.output_dir / filename
        image_dir.mkdir(parents=True, exist_ok=True)
        
        json_path = image_dir / "detections.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(detections, f, indent=4)
        logger.info(f"Saved detections JSON to {json_path}")
        
        orig_path = image_dir / "original.jpg"
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

        det_path = image_dir / "detections.jpg"
        draw_image.save(det_path, "JPEG")
        logger.info(f"Saved detection visualization to {det_path}")

        if detections:
            crop_box = self._clamp_box(detections[0]["box"], original_image.size)
            if crop_box:
                crop_path = image_dir / "crop_001.jpg"
                original_image.crop(crop_box).save(crop_path, "JPEG")
                logger.info(f"Saved first detection crop to {crop_path}")

        experiment_path = image_dir / "experiment.txt"
        max_confidence = max([d["score"] for d in detections]) if detections else 0.0
        with open(experiment_path, "w", encoding="utf-8") as f:
            f.write(f"Image name: {filename}\n")
            f.write(f"Runtime: {runtime_ms:.1f} ms\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Number of detections: {len(detections)}\n")
            f.write(f"Highest confidence: {max_confidence:.4f}\n")
            f.write(f"Model name: {model_name}\n")
            f.write(f"Device: {device}\n")
            if error:
                f.write(f"Error: {error}\n")
        logger.info(f"Saved experiment summary to {experiment_path}")

        return image_dir

    def draw_detection_stages(
        self,
        original_image: Image.Image,
        filename: str,
        stages: Dict[str, List[Dict[str, Any]]],
    ) -> Path:
        """Write raw, filtered, and merged detection files plus overlays."""
        image_dir = self.output_dir / filename
        image_dir.mkdir(parents=True, exist_ok=True)

        for stage_name, detections in stages.items():
            json_path = image_dir / f"detections_{stage_name}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(detections, f, indent=4)

            overlay = original_image.copy()
            draw = ImageDraw.Draw(overlay)
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None

            for det in detections:
                box = det["box"]
                label = det["label"]
                score = det["score"]
                draw.rectangle(box, outline=self._stage_color(stage_name), width=3)
                draw.text(
                    (box[0] + 5, box[1] + 5),
                    f"{label}: {score:.2f}",
                    fill=self._stage_color(stage_name),
                    font=font,
                )

            overlay_path = image_dir / f"detections_{stage_name}.jpg"
            overlay.save(overlay_path, "JPEG")

        return image_dir

    def _clamp_box(self, box: List[int], image_size: tuple[int, int]) -> Optional[tuple[int, int, int, int]]:
        width, height = image_size
        x1 = max(0, min(width, int(box[0])))
        y1 = max(0, min(height, int(box[1])))
        x2 = max(0, min(width, int(box[2])))
        y2 = max(0, min(height, int(box[3])))
        if x2 <= x1 or y2 <= y1:
            return None
        return (x1, y1, x2, y2)

    def _stage_color(self, stage_name: str) -> str:
        colors = {
            "raw": "red",
            "filtered": "yellow",
            "merged": "lime",
            "final": "cyan",
        }
        return colors.get(stage_name, "red")

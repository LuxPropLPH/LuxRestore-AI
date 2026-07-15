import json
from pathlib import Path
from typing import Any, Dict

from PIL import Image


class MaskVisualizer:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def save(
        self,
        image_name: str,
        result: Dict[str, Any],
        device: str,
        model_name: str,
    ) -> Dict[str, Any]:
        import numpy as np

        image = result["image"]
        image_dir = self.output_dir / image_name
        image_dir.mkdir(parents=True, exist_ok=True)

        width, height = image.size
        merged = np.zeros((height, width), dtype=bool)
        mask_count = 0

        for mask in result["masks"]:
            mask_array = np.asarray(mask).astype(bool)
            if mask_array.ndim > 2:
                mask_array = np.squeeze(mask_array)
            merged |= mask_array
            mask_count += 1

        mask_area_percentage = float(merged.sum() / merged.size * 100.0) if merged.size else 0.0

        mask_image = Image.fromarray((merged.astype("uint8") * 255), mode="L")
        mask_path = image_dir / "mask.png"
        mask_image.save(mask_path)

        overlay = self._make_overlay(image, mask_image)
        overlay_path = image_dir / "mask_overlay.jpg"
        overlay.save(overlay_path, "JPEG")

        metadata = {
            "image_name": image_name,
            "model_name": model_name,
            "device": device,
            "runtime_ms": result["runtime_ms"],
            "number_of_prompts": len(result["boxes"]),
            "number_of_masks": mask_count,
            "mask_area_percentage": mask_area_percentage,
            "boxes": result["boxes"],
        }

        metadata_path = image_dir / "mask_metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=4), encoding="utf-8")

        experiment_path = image_dir / "experiment_mask.txt"
        experiment_path.write_text(
            "\n".join(
                [
                    f"Image name: {image_name}",
                    f"Runtime: {result['runtime_ms']:.1f} ms",
                    f"Number of prompts: {len(result['boxes'])}",
                    f"Number of masks: {mask_count}",
                    f"Mask area percentage: {mask_area_percentage:.4f}",
                    f"Device: {device}",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        return metadata

    def _make_overlay(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        base = image.convert("RGBA")
        red = Image.new("RGBA", image.size, (255, 0, 0, 110))
        transparent = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay = Image.composite(red, transparent, mask)
        return Image.alpha_composite(base, overlay).convert("RGB")

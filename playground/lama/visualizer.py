from pathlib import Path

from PIL import Image, ImageDraw


class LaMaVisualizer:
    def save_comparison(self, image_dir: Path) -> Path:
        panels = [
            ("Original", image_dir / "original.jpg"),
            ("GroundingDINO detections", image_dir / "detections_final.jpg"),
            ("SAM2 mask", image_dir / "mask_overlay.jpg"),
            ("Final restored image", image_dir / "restored.png"),
        ]

        images = [Image.open(path).convert("RGB") for _, path in panels]
        target_width = max(img.width for img in images)
        resized = []
        for image in images:
            scale = target_width / image.width
            resized.append(image.resize((target_width, int(image.height * scale))))

        label_height = 34
        total_height = max(img.height for img in resized) + label_height
        comparison = Image.new("RGB", (target_width * len(resized), total_height), "white")
        draw = ImageDraw.Draw(comparison)

        for idx, ((label, _), image) in enumerate(zip(panels, resized)):
            x = idx * target_width
            draw.text((x + 10, 10), label, fill="black")
            comparison.paste(image, (x, label_height))

        output_path = image_dir / "comparison.jpg"
        comparison.save(output_path, "JPEG", quality=92)
        return output_path

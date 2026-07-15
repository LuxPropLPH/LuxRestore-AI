from pathlib import Path
from typing import List
from PIL import Image
import logging

logger = logging.getLogger("grounding_dino_playground.loader")

class ImageLoader:
    def __init__(self, validation_dir: Path):
        self.validation_dir = validation_dir
        self.supported_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    def get_images(self) -> List[Path]:
        """List all supported images in the validation directory."""
        images = []
        if not self.validation_dir.exists():
            logger.warning(f"Validation directory {self.validation_dir} does not exist.")
            return images
        
        for file in self.validation_dir.iterdir():
            if file.suffix.lower() in self.supported_extensions:
                images.append(file)
        return sorted(images)

    def load_image(self, path: Path) -> Image.Image:
        """Load an image using Pillow and convert to RGB format."""
        logger.info(f"Loading image from {path}")
        img = Image.open(path)
        return img.convert("RGB")

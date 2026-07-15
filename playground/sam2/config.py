import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
VALIDATION_DIR = BASE_DIR / "validation"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "weights" / "sam2"

MODEL_ID = "facebook/sam2-hiera-tiny"
DEVICE = os.getenv("DEVICE", "auto")
MASK_THRESHOLD = float(os.getenv("MASK_THRESHOLD", "0.0"))


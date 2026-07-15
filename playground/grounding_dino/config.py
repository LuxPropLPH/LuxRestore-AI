import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
VALIDATION_DIR = BASE_DIR / "validation"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "weights" / "grounding_dino"

# GroundingDINO parameters
MODEL_ID = "IDEA-Research/groundingdino-tiny"
CONFIDENCE_THRESHOLD = float(os.getenv("CONF_THRESHOLD", "0.25"))
DEVICE = os.getenv("DEVICE", "cpu")
PROMPT_TEXT = os.getenv("PROMPT_TEXT", "watermark")

# Ensure directories exist
VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

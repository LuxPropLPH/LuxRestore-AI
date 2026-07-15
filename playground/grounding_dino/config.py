import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
VALIDATION_DIR = BASE_DIR / "validation"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "weights" / "grounding_dino"

# GroundingDINO parameters
MODEL_ID = "IDEA-Research/grounding-dino-tiny"
CONFIDENCE_THRESHOLD = float(os.getenv("CONF_THRESHOLD", "0.25"))
SECONDARY_DETECTION_THRESHOLD = float(os.getenv("SECONDARY_DETECTION_THRESHOLD", "0.30"))
DEVICE = os.getenv("DEVICE", "auto")
PROMPT_TEXT = "gold logo. red text. small watermark."

# Ensure directories exist
VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

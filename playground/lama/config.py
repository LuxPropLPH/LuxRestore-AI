import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "weights" / "lama"
LAMA_REPO_DIR = Path(os.getenv("LAMA_REPO_DIR", r"D:\lama"))

DEVICE = os.getenv("DEVICE", "auto")
MODEL_NAME = "big-lama"
MASK_DILATION_PX = int(os.getenv("LAMA_MASK_DILATION_PX", "11"))

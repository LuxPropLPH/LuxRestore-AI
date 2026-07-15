"""Run real LaMa inpainting from GroundingDINO + SAM2 playground outputs.

Run from the repository root:
    python playground/lama/run.py --image validation/1.jpg
"""

import argparse
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from playground.grounding_dino.utils import setup_logger
from playground.lama import config
from playground.lama.adapter import LaMaAdapter
from playground.lama.model_manager import ModelManager
from playground.lama.visualizer import LaMaVisualizer


logger = setup_logger()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run LaMa restoration for one playground image.")
    parser.add_argument("--image", type=Path, required=True)
    return parser.parse_args()


def resolve_device() -> str:
    import torch

    requested = config.DEVICE.lower()
    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("DEVICE=cuda was requested, but CUDA is not available.")
    if requested not in {"cpu", "cuda"}:
        raise RuntimeError(f"Unsupported DEVICE value '{config.DEVICE}'. Use 'auto', 'cpu', or 'cuda'.")
    return requested


def prepare_lama_input(image_dir: Path, work_dir: Path) -> float:
    original_path = image_dir / "original.jpg"
    mask_path = image_dir / "mask.png"
    if not original_path.exists():
        raise FileNotFoundError(f"Missing original image: {original_path}")
    if not mask_path.exists():
        raise FileNotFoundError(f"Missing SAM2 mask: {mask_path}")

    work_dir.mkdir(parents=True, exist_ok=True)
    image = Image.open(original_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")
    if config.MASK_DILATION_PX > 0:
        mask_array = np.array(mask)
        kernel_size = config.MASK_DILATION_PX * 2 + 1
        kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
        mask_array = cv2.dilate(mask_array, kernel, iterations=1)
        mask = Image.fromarray(mask_array, mode="L")
    image.save(work_dir / "image.png")
    mask.save(work_dir / "image_mask.png")
    mask.save(image_dir / "lama_input_mask.png")

    mask_area = sum(1 for value in mask.getdata() if value > 0)
    return mask_area / (mask.width * mask.height) * 100.0


def main() -> None:
    os.environ.setdefault("PYTHONPATH", str(config.LAMA_REPO_DIR))
    os.environ.setdefault("MPLCONFIGDIR", str(config.BASE_DIR / ".cache" / "matplotlib"))
    args = parse_args()
    image_name = args.image.stem
    image_dir = config.OUTPUT_DIR / image_name

    warnings = []
    device = resolve_device()
    model_path = ModelManager(config.CACHE_DIR).get_model_path()
    work_dir = image_dir / "lama_input"

    logger.info("Preparing LaMa input for %s", image_name)
    mask_area = prepare_lama_input(image_dir, work_dir)

    adapter = LaMaAdapter(config.LAMA_REPO_DIR)
    start_load = time.time()
    adapter.load(model_path, device)
    load_ms = (time.time() - start_load) * 1000.0

    start = time.time()
    restored_bgr = adapter.inpaint(work_dir)
    runtime_ms = (time.time() - start) * 1000.0

    restored_path = image_dir / "restored.png"
    cv2.imwrite(str(restored_path), restored_bgr)
    comparison_path = LaMaVisualizer().save_comparison(image_dir)

    original = Image.open(image_dir / "original.jpg")
    experiment_path = image_dir / "experiment_lama.txt"
    experiment_path.write_text(
        "\n".join(
            [
                f"Runtime: {runtime_ms:.1f} ms",
                f"Model load runtime: {load_ms:.1f} ms",
                f"Device: {device}",
                f"Model: {config.MODEL_NAME}",
                f"Mask area: {mask_area:.4f}%",
                f"Mask dilation: {config.MASK_DILATION_PX}px",
                f"Image size: {original.width}x{original.height}",
                f"Warnings: {'; '.join(warnings) if warnings else 'none'}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    logger.info("Saved restored image to %s", restored_path)
    logger.info("Saved comparison to %s", comparison_path)


if __name__ == "__main__":
    main()

"""Canonical GroundingDINO validation entrypoint.

Run from the repository root:
    python playground/grounding_dino/run.py
"""

import time
import shutil
import argparse
from pathlib import Path
from typing import List
from datetime import datetime
import sys
import importlib

# Add the project root to sys.path to allow running as a script
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from playground.grounding_dino.utils import setup_logger
from playground.grounding_dino import config
from playground.grounding_dino.loader import ImageLoader
from playground.grounding_dino.model_manager import ModelManager
from playground.grounding_dino.postprocess import (
    filter_isolated_detections,
    finalize_detections,
    merge_close_detections,
)


logger = setup_logger()

PROMPT = config.PROMPT_TEXT

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run GroundingDINO watermark validation.")
    parser.add_argument(
        "--image",
        type=Path,
        help="Optional path to one validation image. If omitted, every validation image is processed.",
    )
    return parser.parse_args()

def ensure_runtime_dependencies() -> None:
    """Fail clearly if the GroundingDINO runtime dependencies are unavailable."""
    missing = []
    for module_name in ["PIL", "torch", "transformers"]:
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing.append(module_name)

    if missing:
        missing_list = ", ".join(missing)
        raise RuntimeError(
            f"Missing required playground dependencies: {missing_list}. "
            "Install them with: pip install -r playground/requirements.txt"
        )

def resolve_device() -> str:
    """Resolve CPU/CUDA execution target from config.DEVICE."""
    import torch

    requested_device = config.DEVICE.lower()
    if requested_device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"

    if requested_device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("DEVICE=cuda was requested, but CUDA is not available.")

    if requested_device not in {"cpu", "cuda"}:
        raise RuntimeError(
            f"Unsupported DEVICE value '{config.DEVICE}'. Use 'auto', 'cpu', or 'cuda'."
        )

    return requested_device

def select_images(loader: ImageLoader, image_path: Path | None) -> List[Path]:
    if image_path is None:
        return loader.get_images()

    resolved_path = image_path if image_path.is_absolute() else config.BASE_DIR / image_path
    if not resolved_path.exists():
        raise FileNotFoundError(f"Image not found: {resolved_path}")
    if resolved_path.suffix.lower() not in loader.supported_extensions:
        supported = ", ".join(sorted(loader.supported_extensions))
        raise ValueError(f"Unsupported image extension for {resolved_path}. Supported: {supported}")
    return [resolved_path]

def handle_failure(img_path: Path, error_message: str) -> None:
    """Save failed images/logs to experiments/failures/ directory."""
    failures_dir = Path("experiments") / "failures"
    failures_dir.mkdir(parents=True, exist_ok=True)
    
    dest_img = failures_dir / img_path.name
    try:
        shutil.copy(img_path, dest_img)
    except Exception:
        pass
        
    log_path = failures_dir / f"{img_path.stem}_error.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Image: {img_path.name}\n")
        f.write(f"Error: {error_message}\n")
    logger.warning(f"Saved failure dump for {img_path.name} to {failures_dir}")

def main():
    args = parse_args()
    logger.info("Initializing GroundingDINO technology validation...")
    
    loader = ImageLoader(config.VALIDATION_DIR)
    try:
        images = select_images(loader, args.image)
    except (FileNotFoundError, ValueError) as e:
        logger.error(str(e))
        sys.exit(1)
    
    if not images:
        logger.error(
            "No real validation images found in %s. Add watermarked .jpg, .jpeg, "
            ".png, or .webp files before running GroundingDINO validation.",
            config.VALIDATION_DIR.resolve(),
        )
        sys.exit(1)

    manager = ModelManager(config.CACHE_DIR, config.MODEL_ID)
    try:
        local_model_path = manager.get_local_path()
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    try:
        ensure_runtime_dependencies()
    except RuntimeError as e:
        logger.error(str(e))
        sys.exit(1)

    try:
        device = resolve_device()
    except RuntimeError as e:
        logger.error(str(e))
        sys.exit(1)
    logger.info(f"Using device: {device}")

    from playground.grounding_dino.adapter import HFTransformersAdapter
    from playground.grounding_dino.locator import GroundingDINOLocator
    from playground.grounding_dino.visualizer import ImageVisualizer

    adapter = HFTransformersAdapter()
    locator = GroundingDINOLocator(
        adapter=adapter,
        model_path=local_model_path,
        device=device
    )
    
    try:
        locator.load_model()
    except Exception as e:
        logger.error(f"Error loading GroundingDINO model: {e}")
        sys.exit(1)

    visualizer = ImageVisualizer(config.OUTPUT_DIR)
    
    successes = 0
    failures = 0
    
    for img_path in images:
        logger.info(f"Evaluating Image: {img_path.name} with Prompt: '{PROMPT}'")
        t_start = time.time()
        status = "Success"
        failure_error = None
        raw_detections = []
        filtered_detections = []
        merged_detections = []
        final_detections = []
        pil_img = None

        try:
            pil_img = loader.load_image(img_path)
            raw_detections = locator.locate(
                pil_img,
                prompt=PROMPT,
                threshold=config.CONFIDENCE_THRESHOLD
            )
            filtered_detections = filter_isolated_detections(
                raw_detections,
                secondary_confidence_threshold=config.SECONDARY_DETECTION_THRESHOLD,
                image_size=pil_img.size,
            )
            merged_detections = merge_close_detections(filtered_detections)
            final_detections = finalize_detections(raw_detections, filtered_detections)
            successes += 1
        except Exception as e:
            err_msg = str(e)
            logger.error(f"Failed processing {img_path.name} under prompt '{PROMPT}': {err_msg}")
            status = f"Failed ({type(e).__name__})"
            failure_error = err_msg
            failures += 1
            handle_failure(img_path, f"Prompt: {PROMPT} | Error: {err_msg}")

        elapsed = time.time() - t_start
        runtime_ms = elapsed * 1000.0

        try:
            if pil_img is None:
                pil_img = loader.load_image(img_path)
            visualizer.draw_detections(
                pil_img,
                final_detections,
                prompt=PROMPT,
                filename=img_path.stem,
                runtime_ms=runtime_ms,
                model_name=config.MODEL_ID,
                device=device,
                error=failure_error
            )
            visualizer.draw_detection_stages(
                pil_img,
                filename=img_path.stem,
                stages={
                    "raw": raw_detections,
                    "filtered": filtered_detections,
                    "merged": merged_detections,
                    "final": final_detections,
                },
            )
        except Exception as e:
            logger.error(f"Failed writing outputs for {img_path.name}: {e}")

    logger.info(f"Validation run completed. Successes: {successes}, Failures: {failures}")

if __name__ == "__main__":
    main()

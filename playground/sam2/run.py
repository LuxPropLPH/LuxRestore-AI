"""SAM2 mask validation using GroundingDINO detections.

Run from the repository root:
    python playground/sam2/run.py --image validation/1.jpg
"""

import argparse
import importlib
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from playground.grounding_dino.utils import setup_logger
from playground.sam2 import config
from playground.sam2.adapter import SAM2TransformersAdapter
from playground.sam2.mask_generator import SAM2MaskGenerator
from playground.sam2.model_manager import ModelManager
from playground.sam2.visualizer import MaskVisualizer


logger = setup_logger()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SAM2 mask validation for one image.")
    parser.add_argument(
        "--image",
        type=Path,
        default=config.VALIDATION_DIR / "1.jpg",
        help="Validation image path. Only one image is supported for Ticket 5.1.",
    )
    return parser.parse_args()


def ensure_runtime_dependencies() -> None:
    missing = []
    for module_name in ["PIL", "torch", "transformers", "numpy"]:
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing.append(module_name)

    if missing:
        raise RuntimeError(
            "Missing required SAM2 playground dependencies: "
            + ", ".join(missing)
            + ". Install the playground requirements first."
        )


def resolve_device() -> str:
    import torch

    requested_device = config.DEVICE.lower()
    if requested_device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested_device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("DEVICE=cuda was requested, but CUDA is not available.")
    if requested_device not in {"cpu", "cuda"}:
        raise RuntimeError(f"Unsupported DEVICE value '{config.DEVICE}'. Use 'auto', 'cpu', or 'cuda'.")
    return requested_device


def image_name_from_path(path: Path) -> str:
    resolved = path if path.is_absolute() else config.BASE_DIR / path
    if not resolved.exists():
        raise FileNotFoundError(f"Validation image not found: {resolved}")
    return resolved.stem


def main() -> None:
    args = parse_args()
    logger.info("Initializing SAM2 mask validation...")

    try:
        image_name = image_name_from_path(args.image)
        model_path = ModelManager(config.CACHE_DIR, config.MODEL_ID).get_local_path()
        ensure_runtime_dependencies()
        device = resolve_device()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    adapter = SAM2TransformersAdapter()
    try:
        adapter.load(model_path, device)
        generator = SAM2MaskGenerator(adapter, config.MASK_THRESHOLD)
        result = generator.run(image_name, config.OUTPUT_DIR)
        metadata = MaskVisualizer(config.OUTPUT_DIR).save(
            image_name=image_name,
            result=result,
            device=device,
            model_name=config.MODEL_ID,
        )
    except Exception as e:
        logger.error(f"SAM2 mask generation failed: {e}", exc_info=True)
        sys.exit(1)

    logger.info(
        "SAM2 mask validation complete. Prompts: %s, Masks: %s, Mask area: %.4f%%",
        metadata["number_of_prompts"],
        metadata["number_of_masks"],
        metadata["mask_area_percentage"],
    )


if __name__ == "__main__":
    main()

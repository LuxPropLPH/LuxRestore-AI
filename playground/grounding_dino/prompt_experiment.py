"""Compare GroundingDINO prompts on validation/1.jpg.

Run from the repository root:
    python playground/grounding_dino/prompt_experiment.py
"""

import json
import sys
import time
from pathlib import Path
from typing import Dict, List

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PIL import Image, ImageDraw, ImageFont

from playground.grounding_dino import config
from playground.grounding_dino.adapter import HFTransformersAdapter
from playground.grounding_dino.model_manager import ModelManager
from playground.grounding_dino.run import ensure_runtime_dependencies, resolve_device
from playground.grounding_dino.utils import setup_logger


PROMPTS = [
    "watermark",
    "company logo",
    "logo",
    "text",
    "real estate watermark",
    "property watermark",
    "IMPERA logo",
    "logo text",
    "company logo. text.",
    "gold logo. red text.",
]

THRESHOLDS = [0.25, 0.20]

IMAGE_PATH = config.VALIDATION_DIR / "1.jpg"
OUTPUT_DIR = config.OUTPUT_DIR / "1" / "prompt_experiments"


def main() -> None:
    logger = setup_logger()
    ensure_runtime_dependencies()
    device = resolve_device()
    model_path = ModelManager(config.CACHE_DIR, config.MODEL_ID).get_local_path()

    adapter = HFTransformersAdapter()
    adapter.load(model_path, device)
    image = Image.open(IMAGE_PATH).convert("RGB")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for prompt in PROMPTS:
        for threshold in THRESHOLDS:
            start = time.time()
            detections = adapter.detect(image, prompt=prompt, threshold=threshold)
            runtime_ms = (time.time() - start) * 1000.0
            slug = _slug(prompt, threshold)
            prompt_dir = OUTPUT_DIR / slug
            prompt_dir.mkdir(parents=True, exist_ok=True)

            _write_detection_artifacts(prompt_dir, image, detections)
            row = {
                "prompt": prompt,
                "threshold": threshold,
                "runtime_ms": runtime_ms,
                "box_count": len(detections),
                "max_confidence": max([d["score"] for d in detections], default=0.0),
                "detections": detections,
                "gold_logo_detected": _gold_logo_detected(detections),
                "red_text_detected": _red_text_detected(detections),
                "false_positive_count": _false_positive_count(detections),
            }
            rows.append(row)
            logger.info(
                "%s @ %.2f -> boxes=%s max=%.4f logo=%s text=%s fp=%s",
                prompt,
                threshold,
                row["box_count"],
                row["max_confidence"],
                row["gold_logo_detected"],
                row["red_text_detected"],
                row["false_positive_count"],
            )

    report_path = OUTPUT_DIR / "comparison.md"
    report_path.write_text(_format_report(rows), encoding="utf-8")
    (OUTPUT_DIR / "comparison.json").write_text(json.dumps(rows, indent=4), encoding="utf-8")
    logger.info(f"Wrote prompt comparison report to {report_path}")


def _write_detection_artifacts(
    prompt_dir: Path,
    image: Image.Image,
    detections: List[Dict],
) -> None:
    (prompt_dir / "detections.json").write_text(json.dumps(detections, indent=4), encoding="utf-8")
    image.save(prompt_dir / "original.jpg", "JPEG")

    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for detection in detections:
        box = detection["box"]
        draw.rectangle(box, outline="red", width=3)
        draw.text((box[0] + 5, box[1] + 5), f"{detection['score']:.2f}", fill="red", font=font)
    overlay.save(prompt_dir / "detections.jpg", "JPEG")


def _format_report(rows: List[Dict]) -> str:
    lines = [
        "# GroundingDINO Prompt Comparison",
        "",
        f"- Image: `{IMAGE_PATH}`",
        f"- Model: `{config.MODEL_ID}`",
        "",
        "| Prompt | Threshold | Boxes | Max Confidence | Gold Logo Detected | Red Text Detected | False Positives | Runtime (ms) |",
        "|---|---:|---:|---:|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {prompt} | {threshold:.2f} | {box_count} | {max_confidence:.4f} | {gold_logo_detected} | {red_text_detected} | {false_positive_count} | {runtime_ms:.1f} |".format(
                **row
            )
        )
    lines.append("")
    lines.append(_recommendation(rows))
    return "\n".join(lines)


def _recommendation(rows: List[Dict]) -> str:
    complete = [row for row in rows if row["gold_logo_detected"] and row["red_text_detected"]]
    if not complete:
        return (
            "## Recommendation\n\n"
            "No tested prompt/threshold combination captured both the gold logo and red text. "
            "Do not continue to SAM2 for full watermark removal from this detector output yet."
        )

    best = sorted(
        complete,
        key=lambda row: (row["false_positive_count"], -row["max_confidence"], row["box_count"]),
    )[0]
    return (
        "## Recommendation\n\n"
        f"Use prompt `{best['prompt']}` with threshold `{best['threshold']:.2f}`. "
        "It captured both watermark components with the cleanest observed result."
    )


def _gold_logo_detected(detections: List[Dict]) -> bool:
    # Gold diamond/logo is visually around x=260-315, y=195-250 on validation/1.jpg.
    target = (250, 185, 320, 260)
    return any(_iou(det["box"], target) > 0.05 or _center_in(det["box"], target) for det in detections)


def _red_text_detected(detections: List[Dict]) -> bool:
    # Red IMPERA text is visually around x=310-415, y=213-240 on validation/1.jpg.
    target = (305, 205, 425, 245)
    return any(_iou(det["box"], target) > 0.10 or _center_in(det["box"], target) for det in detections)


def _false_positive_count(detections: List[Dict]) -> int:
    count = 0
    for detection in detections:
        if not _gold_logo_detected([detection]) and not _red_text_detected([detection]):
            count += 1
    return count


def _center_in(box: List[int], target: tuple[int, int, int, int]) -> bool:
    cx = (box[0] + box[2]) / 2.0
    cy = (box[1] + box[3]) / 2.0
    return target[0] <= cx <= target[2] and target[1] <= cy <= target[3]


def _iou(box: List[int], target: tuple[int, int, int, int]) -> float:
    x1 = max(box[0], target[0])
    y1 = max(box[1], target[1])
    x2 = min(box[2], target[2])
    y2 = min(box[3], target[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area_box = max(0, box[2] - box[0]) * max(0, box[3] - box[1])
    area_target = max(0, target[2] - target[0]) * max(0, target[3] - target[1])
    union = area_box + area_target - inter
    return inter / union if union else 0.0


def _slug(prompt: str, threshold: float) -> str:
    safe_prompt = "".join(ch if ch.isalnum() else "_" for ch in prompt.lower()).strip("_")
    return f"{safe_prompt}_thr_{str(threshold).replace('.', '_')}"


if __name__ == "__main__":
    main()

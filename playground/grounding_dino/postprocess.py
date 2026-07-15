from typing import Any, Dict, List


Detection = Dict[str, Any]


def filter_isolated_detections(
    detections: List[Detection],
    max_group_gap_px: int = 45,
    secondary_confidence_threshold: float = 0.30,
    image_size: tuple[int, int] | None = None,
) -> List[Detection]:
    """Remove isolated false positives while preserving plausible watermark fragments."""
    if len(detections) <= 2:
        return detections

    filtered = []
    for detection in detections:
        has_neighbor = any(
            other is not detection
            and _box_distance(detection["box"], other["box"]) <= max_group_gap_px
            for other in detections
        )
        if has_neighbor or _is_valid_secondary_detection(
            detection,
            secondary_confidence_threshold,
            image_size,
        ):
            filtered.append(detection)
    return filtered


def finalize_detections(
    raw_detections: List[Detection],
    filtered_detections: List[Detection],
    max_group_gap_px: int = 45,
) -> List[Detection]:
    """Merge the primary close group and keep valid isolated secondary detections separate."""
    merged_groups = merge_close_detections(filtered_detections, max_group_gap_px)
    return merged_groups


def merge_close_detections(
    detections: List[Detection],
    max_group_gap_px: int = 45,
) -> List[Detection]:
    """Merge close detections into one region for SAM2 box prompting."""
    remaining = list(detections)
    merged = []

    while remaining:
        seed = remaining.pop(0)
        group = [seed]
        changed = True

        while changed:
            changed = False
            for candidate in list(remaining):
                if any(
                    _box_distance(candidate["box"], member["box"]) <= max_group_gap_px
                    for member in group
                ):
                    group.append(candidate)
                    remaining.remove(candidate)
                    changed = True

        merged.append(_merge_group(group))

    return merged


def _merge_group(group: List[Detection]) -> Detection:
    x1 = min(detection["box"][0] for detection in group)
    y1 = min(detection["box"][1] for detection in group)
    x2 = max(detection["box"][2] for detection in group)
    y2 = max(detection["box"][3] for detection in group)
    labels = [str(detection["label"]) for detection in group]
    score = max(float(detection["score"]) for detection in group)

    return {
        "box": [x1, y1, x2, y2],
        "score": round(score, 4),
        "label": "+".join(labels),
        "metadata": {
            "merged": len(group) > 1,
            "source_count": len(group),
            "source_labels": labels,
        },
    }


def _is_valid_secondary_detection(
    detection: Detection,
    confidence_threshold: float,
    image_size: tuple[int, int] | None,
) -> bool:
    label = str(detection.get("label", "")).lower()
    if not any(token in label for token in ("watermark", "text", "logo")):
        return False

    if float(detection.get("score", 0.0)) < confidence_threshold:
        return False

    box = detection["box"]
    width = max(0, box[2] - box[0])
    height = max(0, box[3] - box[1])
    if width == 0 or height == 0:
        return False

    area = width * height
    aspect_ratio = width / height
    if area < 80 or area > 12000:
        return False
    if aspect_ratio < 0.25 or aspect_ratio > 8.0:
        return False

    if image_size is not None:
        image_width, image_height = image_size
        margin_x = image_width * 0.05
        margin_y = image_height * 0.05
        ceiling_cutoff = image_height * 0.18
        center_x = (box[0] + box[2]) / 2.0
        center_y = (box[1] + box[3]) / 2.0

        if center_y < ceiling_cutoff:
            return False
        if center_x < margin_x or center_x > image_width - margin_x:
            return False
        if center_y < margin_y or center_y > image_height - margin_y:
            return False

    return True


def _box_distance(a: List[int], b: List[int]) -> float:
    if _boxes_overlap_or_touch(a, b):
        return 0.0

    horizontal_gap = max(a[0] - b[2], b[0] - a[2], 0)
    vertical_gap = max(a[1] - b[3], b[1] - a[3], 0)
    return (horizontal_gap**2 + vertical_gap**2) ** 0.5


def _boxes_overlap_or_touch(a: List[int], b: List[int]) -> bool:
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])

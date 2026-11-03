from __future__ import annotations

from math import isfinite
from typing import Any


def adapt_arduino_detections(
    output: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Convert Arduino Object Detection output into
    the format expected by Smart Speed Guard.

    Arduino confidence: percentage (0–100)
    Project confidence: fraction (0–1)

    Bounding boxes are preserved in XYXY format.
    """

    if not isinstance(output, dict):
        raise ValueError("Detection output must be a dictionary")

    raw_detections = output.get("detection", [])

    if not isinstance(raw_detections, list):
        raise ValueError("'detection' must be a list")

    adapted = []

    for index, detection in enumerate(raw_detections):
        if not isinstance(detection, dict):
            raise ValueError(
                f"Detection {index} must be a dictionary"
            )

        class_name = detection.get("class_name")
        confidence = detection.get("confidence")
        bounding_box = detection.get("bounding_box_xyxy")

        if not isinstance(class_name, str) or not class_name.strip():
            raise ValueError(
                f"Detection {index} has an invalid class_name"
            )

        if (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not isfinite(confidence)
            or not 0 <= confidence <= 100
        ):
            raise ValueError(
                f"Detection {index} has invalid confidence"
            )

        if (
            not isinstance(bounding_box, (list, tuple))
            or len(bounding_box) != 4
        ):
            raise ValueError(
                f"Detection {index} has an invalid bounding box"
            )

        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not isfinite(value)
            for value in bounding_box
        ):
            raise ValueError(
                f"Detection {index} has non-numeric bounding box coordinates"
            )

        adapted.append({
            "class_name": class_name.strip().lower(),
            "confidence": float(confidence) / 100.0,
            "bounding_box_xyxy": [
                float(value) for value in bounding_box
            ],
        })

    return adapted
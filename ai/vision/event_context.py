
from __future__ import annotations

from math import isfinite
from typing import Any


SUPPORTED_OBJECTS = {
    "person",
    "car",
    "motorcycle",
    "bicycle",
    "bus",
    "truck",
    "other",
}


def create_event_context(
    event_id: int,
    timestamp: int,
    alert_type: str,
    detections: list[dict[str, Any]],
    min_confidence: float = 0.50,
) -> dict[str, Any]:

    if not isinstance(event_id, int) or isinstance(event_id, bool) or event_id < 0:
        raise ValueError("event_id must be a non-negative integer")

    if not isinstance(timestamp, int) or isinstance(timestamp, bool) or timestamp < 0:
        raise ValueError("timestamp must be a non-negative integer")

    if not isinstance(alert_type, str) or not alert_type.strip():
        raise ValueError("alert_type must be a non-empty string")

    if not isinstance(detections, list):
        raise ValueError("detections must be a list")

    if (
        not isinstance(min_confidence, (int, float))
        or isinstance(min_confidence, bool)
        or not isfinite(min_confidence)
    ):
        raise ValueError("min_confidence must be numeric")

    if not 0.0 <= min_confidence <= 1.0:
        raise ValueError("min_confidence must be between 0 and 1")

    object_counts = {name: 0 for name in SUPPORTED_OBJECTS}
    accepted_detections = []

    for detection in detections:
        if not isinstance(detection, dict):
            raise ValueError("Each detection must be a dictionary")

        if "class_name" not in detection or "confidence" not in detection:
            raise ValueError("Detection requires class_name and confidence")

        class_name = detection["class_name"]
        confidence = detection["confidence"]

        if not isinstance(class_name, str) or not class_name.strip():
            raise ValueError("class_name must be a non-empty string")

        if (
            not isinstance(confidence, (int, float))
            or isinstance(confidence, bool)
            or not isfinite(confidence)
        ):
            raise ValueError("confidence must be numeric")

        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

        class_name = class_name.strip().lower()

        if confidence < min_confidence:
            continue

        if class_name not in SUPPORTED_OBJECTS:
            class_name = "other"

        object_counts[class_name] += 1

        accepted_detection = {
            "class_name": class_name,
            "confidence": float(confidence),
        }

        if "bounding_box_xyxy" in detection:
            bounding_box = detection["bounding_box_xyxy"]

            if (
                not isinstance(bounding_box, (list, tuple))
                or len(bounding_box) != 4
            ):
                raise ValueError(
                    "bounding_box_xyxy must contain four coordinates"
                )

            if any(
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not isfinite(value)
                for value in bounding_box
            ):
                raise ValueError(
                    "Bounding-box coordinates must be finite numbers"
                )

            x1, y1, x2, y2 = bounding_box

            if x2 < x1 or y2 < y1:
                raise ValueError("Invalid XYXY bounding-box coordinates")

            accepted_detection["bounding_box_xyxy"] = [
                float(value) for value in bounding_box
            ]

        accepted_detections.append(accepted_detection)

    return {
        "event_id": event_id,
        "timestamp": timestamp,
        "alert_type": alert_type.strip().upper(),
        "visual_context": object_counts,
        "detections": accepted_detections,
        "detection_count": len(accepted_detections),
    }

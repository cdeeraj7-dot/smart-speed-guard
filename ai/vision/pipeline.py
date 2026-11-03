
from __future__ import annotations

from typing import Any

from ai.vision.arduino_adapter import adapt_arduino_detections
from ai.vision.event_context import create_event_context
from ai.vision.trigger import VisualTrigger


class VisionEventPipeline:
    """
    Connects safety-event triggering with visual event context.

    Arduino detections are converted through the adapter.
    Camera capture and model inference remain external.
    """

    def __init__(
        self,
        cooldown_ms: int = 2_000,
        min_confidence: float = 0.50,
    ):
        self.trigger = VisualTrigger(cooldown_ms=cooldown_ms)
        self.min_confidence = min_confidence
        self.next_event_id = 1

    def process(
        self,
        record: dict[str, Any],
        detections: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        trigger_result = self.trigger.process(record)

        if not trigger_result["capture_requested"]:
            return {
                "capture_requested": False,
                "event_context": None,
            }

        alert_type = record.get("alert_type", "UNKNOWN")

        event_context = create_event_context(
            event_id=self.next_event_id,
            timestamp=record["timestamp"],
            alert_type=alert_type,
            detections=detections if detections is not None else [],
            min_confidence=self.min_confidence,
        )

        self.next_event_id += 1

        return {
            "capture_requested": True,
            "event_context": event_context,
        }

    def process_arduino_output(
        self,
        record: dict[str, Any],
        arduino_output: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process raw Arduino Object Detection output
        through the existing vision event pipeline.
        """

        detections = adapt_arduino_detections(arduino_output)

        return self.process(
            record=record,
            detections=detections,
        )

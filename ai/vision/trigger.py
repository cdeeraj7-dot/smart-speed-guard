from __future__ import annotations

from typing import Any


class VisualTrigger:
    """
    Generates camera capture requests when a new
    deterministic safety alert is detected.

    This module does not control the safety system
    or directly access the camera.
    """

    def __init__(self, cooldown_ms: int = 2_000):
        if cooldown_ms < 0:
            raise ValueError("cooldown_ms cannot be negative")

        self.cooldown_ms = cooldown_ms
        self.previous_alert = 0
        self.last_capture_timestamp: int | None = None

    def process(self, record: dict[str, Any]) -> dict[str, Any]:
        if "timestamp" not in record:
            raise ValueError("Missing timestamp field")

        if "deterministic_alert" not in record:
            raise ValueError("Missing deterministic_alert field")

        timestamp = record["timestamp"]
        alert = record["deterministic_alert"]

        if not isinstance(timestamp, int) or isinstance(timestamp, bool):
            raise ValueError("timestamp must be an integer")

        if timestamp < 0:
            raise ValueError("timestamp cannot be negative")

        if not isinstance(alert, int) or isinstance(alert, bool):
            raise ValueError("deterministic_alert must be an integer")

        if alert < 0:
            raise ValueError("deterministic_alert cannot be negative")

        if (
            self.last_capture_timestamp is not None
            and timestamp < self.last_capture_timestamp
        ):
            raise ValueError("Records must be processed chronologically")

        new_alert = alert != 0 and alert != self.previous_alert

        capture_requested = False

        if new_alert:
            cooldown_complete = (
                self.last_capture_timestamp is None
                or timestamp - self.last_capture_timestamp >= self.cooldown_ms
            )

            if cooldown_complete:
                capture_requested = True
                self.last_capture_timestamp = timestamp

        self.previous_alert = alert

        return {
            "timestamp": timestamp,
            "deterministic_alert": alert,
            "capture_requested": capture_requested,
        }
from __future__ import annotations

from typing import Any


def analyze_event_frequency(
    records: list[dict[str, Any]],
    interval_ms: int = 60_000,
) -> list[dict[str, int | float]]:
    """
    Analyze the frequency of deterministic safety events.

    A new event is counted when the alert state changes
    from inactive to active, or when the active alert type
    changes.

    Repeated telemetry records containing the same active
    alert are not counted as separate events.

    Events are grouped into fixed time intervals.

    Args:
        records: Telemetry records containing timestamp
                 and deterministic_alert.
        interval_ms: Duration of each analysis interval.

    Returns:
        A list of time intervals containing event counts
        and events-per-minute rates.
    """

    if interval_ms <= 0:
        raise ValueError("interval_ms must be positive")

    if not records:
        return []

    for record in records:
        if "timestamp" not in record:
            raise ValueError("Missing timestamp field")

        if "deterministic_alert" not in record:
            raise ValueError("Missing deterministic_alert field")

        if record["timestamp"] < 0:
            raise ValueError("Timestamp cannot be negative")

        if not isinstance(record["deterministic_alert"], int):
            raise ValueError("deterministic_alert must be an integer")

        if record["deterministic_alert"] < 0:
            raise ValueError("Alert value cannot be negative")

    sorted_records = sorted(
        records,
        key=lambda record: record["timestamp"],
    )

    start_time = sorted_records[0]["timestamp"]
    end_time = sorted_records[-1]["timestamp"]

    total_intervals = (
        (end_time - start_time) // interval_ms
    ) + 1

    event_counts = [0] * total_intervals

    previous_alert = 0

    for record in sorted_records:
        current_alert = record["deterministic_alert"]

        new_event = (
            current_alert != 0
            and current_alert != previous_alert
        )

        if new_event:
            interval_index = (
                (record["timestamp"] - start_time)
                // interval_ms
            )

            event_counts[interval_index] += 1

        previous_alert = current_alert

    results = []

    for index, event_count in enumerate(event_counts):
        window_start = start_time + index * interval_ms
        window_end = window_start + interval_ms

        events_per_minute = (
            event_count * 60_000 / interval_ms
        )

        results.append({
            "window_start_ms": window_start,
            "window_end_ms": window_end,
            "event_count": event_count,
            "events_per_minute": events_per_minute,
        })

    return results
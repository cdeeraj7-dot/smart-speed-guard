from __future__ import annotations

from typing import Any


def calculate_risk_profile(
    event_windows: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Generate an interpretable driving-risk profile
    from event-frequency analysis.

    Risk levels are provisional development categories,
    not experimentally validated safety thresholds.
    """

    if not event_windows:
        return {
            "risk_score": 0,
            "risk_level": "INSUFFICIENT_DATA",
            "total_events": 0,
            "average_events_per_minute": 0.0,
            "observation_duration_ms": 0,
        }

    required_fields = {
        "window_start_ms",
        "window_end_ms",
        "event_count",
        "events_per_minute",
    }

    for window in event_windows:
        missing = required_fields - window.keys()

        if missing:
            raise ValueError(
                f"Missing fields: {sorted(missing)}"
            )

        if window["event_count"] < 0:
            raise ValueError("event_count cannot be negative")

        if window["window_end_ms"] <= window["window_start_ms"]:
            raise ValueError("Invalid time window")

        if window["events_per_minute"] < 0:
            raise ValueError("Event rate cannot be negative")

    total_events = sum(
        window["event_count"] for window in event_windows
    )

    start_time = min(
        window["window_start_ms"] for window in event_windows
    )

    end_time = max(
        window["window_end_ms"] for window in event_windows
    )

    observation_duration_ms = end_time - start_time

    total_minutes = observation_duration_ms / 60_000

    average_rate = (
        total_events / total_minutes
        if total_minutes > 0
        else 0.0
    )

    # Provisional development scoring.
    # These values must be calibrated using real driving data.
    risk_score = min(round(average_rate * 10), 100)

    if risk_score < 20:
        risk_level = "LOW"
    elif risk_score < 50:
        risk_level = "MODERATE"
    elif risk_score < 80:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "total_events": total_events,
        "average_events_per_minute": round(average_rate, 2),
        "observation_duration_ms": observation_duration_ms,
    }
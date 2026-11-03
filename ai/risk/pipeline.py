from __future__ import annotations

from typing import Any

from ai.risk.event_frequency import analyze_event_frequency
from ai.risk.risk_profiler import calculate_risk_profile


def generate_driving_risk_profile(
    records: list[dict[str, Any]],
    interval_ms: int = 60_000,
) -> dict[str, Any]:
    """
    Process telemetry records and generate a driving-risk profile.

    This is an AI analysis layer. It does not replace or
    override deterministic safety alerts.
    """

    if interval_ms <= 0:
        raise ValueError("interval_ms must be positive")

    if not records:
        return calculate_risk_profile([])

    event_windows = analyze_event_frequency(
        records,
        interval_ms=interval_ms,
    )

    risk_profile = calculate_risk_profile(event_windows)

    return {
        **risk_profile,
        "event_windows": event_windows,
    }
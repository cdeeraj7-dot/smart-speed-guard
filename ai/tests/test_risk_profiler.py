import pytest

from ai.risk.risk_profiler import calculate_risk_profile


def make_window(start, end, event_count, events_per_minute=None):
    duration_minutes = (end - start) / 60_000
    if events_per_minute is None:
        events_per_minute = event_count / duration_minutes

    return {
        "window_start_ms": start,
        "window_end_ms": end,
        "event_count": event_count,
        "events_per_minute": events_per_minute,
    }

def test_empty_windows_return_insufficient_data():
    assert calculate_risk_profile([]) == {
        "risk_score": 0,
        "risk_level": "INSUFFICIENT_DATA",
        "total_events": 0,
        "average_events_per_minute": 0.0,
        "observation_duration_ms": 0,
    }


def test_calculates_profile_from_event_windows():
    result = calculate_risk_profile(
        [
            make_window(0, 60_000, 1),
            make_window(60_000, 120_000, 2),
        ]
    )

    assert result == {
        "risk_score": 15,
        "risk_level": "LOW",
        "total_events": 3,
        "average_events_per_minute": 1.5,
        "observation_duration_ms": 120_000,
    }


@pytest.mark.parametrize(
    ("event_count", "expected_score", "expected_level"),
    [
        (2, 20, "MODERATE"),
        (5, 50, "HIGH"),
        (8, 80, "CRITICAL"),
        (12, 100, "CRITICAL"),
    ],
)
def test_assigns_risk_level_at_score_boundaries(
    event_count,
    expected_score,
    expected_level,
):
    result = calculate_risk_profile([make_window(0, 60_000, event_count)])

    assert result["risk_score"] == expected_score
    assert result["risk_level"] == expected_level


@pytest.mark.parametrize(
    ("windows", "message"),
    [
        ([{"window_start_ms": 0}], "Missing fields"),
        (
            [make_window(0, 60_000, -1)],
            "event_count cannot be negative",
        ),
        (
            [make_window(60_000, 60_000, 0, events_per_minute=0)],
            "Invalid time window",
        ),
        (
            [make_window(0, 60_000, 0, events_per_minute=-1)],
            "Event rate cannot be negative",
        ),
    ],
)
def test_rejects_invalid_windows(windows, message):
    with pytest.raises(ValueError, match=message):
        calculate_risk_profile(windows)

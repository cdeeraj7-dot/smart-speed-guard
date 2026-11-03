import pytest

from ai.risk.pipeline import generate_driving_risk_profile


def make_record(timestamp, alert):
    return {
        "timestamp": timestamp,
        "deterministic_alert": alert,
    }


def test_empty_records_return_insufficient_data_profile():
    assert generate_driving_risk_profile([]) == {
        "risk_score": 0,
        "risk_level": "INSUFFICIENT_DATA",
        "total_events": 0,
        "average_events_per_minute": 0.0,
        "observation_duration_ms": 0,
    }


def test_generates_profile_and_includes_event_windows():
    result = generate_driving_risk_profile(
        [
            make_record(0, 0),
            make_record(30_000, 1),
            make_record(60_000, 1),
            make_record(90_000, 0),
            make_record(120_000, 2),
        ]
    )

    assert result["total_events"] == 2
    assert result["average_events_per_minute"] == 0.67
    assert result["risk_score"] == 7
    assert result["risk_level"] == "LOW"
    assert result["observation_duration_ms"] == 180_000
    assert [window["event_count"] for window in result["event_windows"]] == [
        1,
        0,
        1,
    ]


def test_custom_interval_is_passed_through():
    result = generate_driving_risk_profile(
        [make_record(0, 1)],
        interval_ms=30_000,
    )

    assert result["event_windows"] == [
        {
            "window_start_ms": 0,
            "window_end_ms": 30_000,
            "event_count": 1,
            "events_per_minute": 2.0,
        }
    ]


def test_invalid_input_is_reported():
    with pytest.raises(ValueError, match="interval_ms must be positive"):
        generate_driving_risk_profile([], interval_ms=0)

    with pytest.raises(ValueError, match="Missing timestamp field"):
        generate_driving_risk_profile([{"deterministic_alert": 1}])

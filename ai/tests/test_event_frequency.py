import pytest

from ai.risk.event_frequency import analyze_event_frequency


def make_record(timestamp, alert):
    return {
        "timestamp": timestamp,
        "deterministic_alert": alert,
    }


def test_empty_records():
    assert analyze_event_frequency([]) == []


def test_counts_alert_activations_and_type_changes_only():
    records = [
        make_record(0, 0),
        make_record(1000, 1),
        make_record(2000, 1),
        make_record(3000, 2),
        make_record(4000, 0),
        make_record(5000, 2),
    ]

    result = analyze_event_frequency(records)

    assert result == [
        {
            "window_start_ms": 0,
            "window_end_ms": 60_000,
            "event_count": 3,
            "events_per_minute": 3.0,
        }
    ]


def test_sorts_records_and_groups_events_into_intervals():
    records = [
        make_record(60_000, 1),
        make_record(0, 1),
        make_record(120_000, 2),
    ]

    result = analyze_event_frequency(records)

    assert [window["event_count"] for window in result] == [1, 0, 1]
    assert [window["window_start_ms"] for window in result] == [
        0,
        60_000,
        120_000,
    ]


def test_calculates_rate_for_custom_interval():
    result = analyze_event_frequency(
        [make_record(0, 1)],
        interval_ms=30_000,
    )

    assert result[0]["events_per_minute"] == 2.0


@pytest.mark.parametrize(
    ("records", "interval_ms", "message"),
    [
        ([], 0, "interval_ms must be positive"),
        ([{"deterministic_alert": 0}], 60_000, "Missing timestamp field"),
        ([{"timestamp": 0}], 60_000, "Missing deterministic_alert field"),
        (
            [make_record(-1, 0)],
            60_000,
            "Timestamp cannot be negative",
        ),
        (
            [make_record(0, 1.0)],
            60_000,
            "deterministic_alert must be an integer",
        ),
        (
            [make_record(0, -1)],
            60_000,
            "Alert value cannot be negative",
        ),
    ],
)
def test_rejects_invalid_input(records, interval_ms, message):
    with pytest.raises(ValueError, match=message):
        analyze_event_frequency(records, interval_ms=interval_ms)

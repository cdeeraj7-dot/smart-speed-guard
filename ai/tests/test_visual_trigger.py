import pytest

from ai.vision.trigger import VisualTrigger


def make_record(timestamp, alert):
    return {
        "timestamp": timestamp,
        "deterministic_alert": alert,
    }


def test_requests_capture_for_first_active_alert():
    trigger = VisualTrigger()

    assert trigger.process(make_record(100, 1)) == {
        "timestamp": 100,
        "deterministic_alert": 1,
        "capture_requested": True,
    }


def test_repeated_alert_does_not_request_another_capture():
    trigger = VisualTrigger()

    trigger.process(make_record(100, 1))

    assert trigger.process(make_record(500, 1))["capture_requested"] is False


def test_new_alert_type_requests_capture_after_cooldown():
    trigger = VisualTrigger(cooldown_ms=2_000)

    trigger.process(make_record(100, 1))
    result = trigger.process(make_record(2_100, 2))

    assert result["capture_requested"] is True


def test_new_alert_type_is_suppressed_during_cooldown():
    trigger = VisualTrigger(cooldown_ms=2_000)

    trigger.process(make_record(100, 1))
    result = trigger.process(make_record(2_099, 2))

    assert result["capture_requested"] is False


def test_alert_after_inactive_state_requests_capture():
    trigger = VisualTrigger()

    trigger.process(make_record(100, 1))
    trigger.process(make_record(200, 0))

    assert trigger.process(make_record(2_100, 1))["capture_requested"] is True


def test_zero_cooldown_allows_immediate_new_alert_capture():
    trigger = VisualTrigger(cooldown_ms=0)

    trigger.process(make_record(100, 1))
    trigger.process(make_record(200, 0))

    assert trigger.process(make_record(200, 2))["capture_requested"] is True


@pytest.mark.parametrize(
    ("record", "message"),
    [
        ({"deterministic_alert": 1}, "Missing timestamp field"),
        ({"timestamp": 0}, "Missing deterministic_alert field"),
        (
            make_record(True, 1),
            "timestamp must be an integer",
        ),
        (
            make_record(-1, 1),
            "timestamp cannot be negative",
        ),
        (
            make_record(0, True),
            "deterministic_alert must be an integer",
        ),
        (
            make_record(0, 1.0),
            "deterministic_alert must be an integer",
        ),
        (
            make_record(0, -1),
            "deterministic_alert cannot be negative",
        ),
    ],
)
def test_rejects_invalid_records(record, message):
    with pytest.raises(ValueError, match=message):
        VisualTrigger().process(record)


def test_rejects_negative_cooldown():
    with pytest.raises(ValueError, match="cooldown_ms cannot be negative"):
        VisualTrigger(cooldown_ms=-1)


def test_rejects_timestamp_before_last_capture():
    trigger = VisualTrigger()
    trigger.process(make_record(100, 1))

    with pytest.raises(
        ValueError,
        match="Records must be processed chronologically",
    ):
        trigger.process(make_record(99, 2))

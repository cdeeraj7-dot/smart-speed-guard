from firmware.linux.bridge_contract import (
    EXPECTED_CALLBACK_ARG_COUNT,
    MCU_TELEMETRY_FIELDS,
    OBSTACLE_DISTANCE_UNAVAILABLE,
    VALID_ALERT_IDS,
    validate_callback_payload,
)


def make_valid_payload(**overrides):
    field_names = [
        "mcu_timestamp_ms",
        "speed_hall",
        "speed_gps",
        "latitude",
        "longitude",
        "gps_valid",
        "accel_x",
        "accel_y",
        "accel_z",
        "gyro_x",
        "gyro_y",
        "gyro_z",
        "gyro_valid",
        "obstacle_distance",
        "deterministic_alert",
        "sensor_valid",
    ]
    payload = (
        1234,
        42.5,
        40.0,
        12.34,
        56.78,
        True,
        0.05,
        -0.01,
        0.96,
        0.0,
        0.0,
        0.0,
        False,
        2.5,
        1,
        True,
    )
    values = list(payload)
    for field_name, value in overrides.items():
        values[field_names.index(field_name)] = value
    return tuple(values)


def test_current_bridge_schema_has_expected_field_count():
    assert len(MCU_TELEMETRY_FIELDS) == 16
    assert EXPECTED_CALLBACK_ARG_COUNT == 16


def test_validate_callback_payload_accepts_current_schema():
    assert validate_callback_payload(make_valid_payload()) == []


def test_validate_callback_payload_accepts_valid_boundary_values():
    assert validate_callback_payload(make_valid_payload(mcu_timestamp_ms=0, deterministic_alert=0)) == []
    assert validate_callback_payload(make_valid_payload(deterministic_alert=max(VALID_ALERT_IDS))) == []


def test_validate_callback_payload_accepts_unavailable_distance_sentinel():
    assert validate_callback_payload(
        make_valid_payload(obstacle_distance=OBSTACLE_DISTANCE_UNAVAILABLE)
    ) == []


def test_validate_callback_payload_rejects_other_negative_distances():
    assert validate_callback_payload(make_valid_payload(obstacle_distance=-2.0))


def test_validate_callback_payload_rejects_wrong_length():
    payload = (1, 2, 3)
    assert validate_callback_payload(payload)


def test_validate_callback_payload_rejects_wrong_types():
    payload = (
        1,
        2.0,
        2.0,
        0.0,
        0.0,
        "yes",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        False,
        3.0,
        0,
        True,
    )

    errors = validate_callback_payload(payload)
    assert any("gps_valid must be boolean" in error for error in errors)


def test_validate_callback_payload_rejects_negative_and_boolean_timestamps():
    assert validate_callback_payload(make_valid_payload(mcu_timestamp_ms=-1))
    assert validate_callback_payload(make_valid_payload(mcu_timestamp_ms=True))


def test_validate_callback_payload_rejects_nonfinite_numeric_values():
    for bad_value in (float("nan"), float("inf"), float("-inf")):
        assert validate_callback_payload(make_valid_payload(speed_hall=bad_value))
        assert validate_callback_payload(make_valid_payload(latitude=bad_value))
        assert validate_callback_payload(make_valid_payload(obstacle_distance=bad_value))


def test_validate_callback_payload_rejects_invalid_alert_ids():
    assert validate_callback_payload(make_valid_payload(deterministic_alert=4))
    assert validate_callback_payload(make_valid_payload(deterministic_alert=True))

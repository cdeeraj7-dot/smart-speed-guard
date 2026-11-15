from __future__ import annotations

import math
from typing import Sequence

MCU_TELEMETRY_FIELDS = (
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
)

CSV_COLUMNS = MCU_TELEMETRY_FIELDS
EXPECTED_CALLBACK_ARG_COUNT = len(MCU_TELEMETRY_FIELDS)
VALID_ALERT_IDS = {0, 1, 2, 3}


def _is_finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _is_int_field(value: object) -> bool:
    return type(value) is int


def validate_callback_payload(payload: Sequence[object]) -> list[str]:
    """Validate the current MCU-to-Linux callback payload contract.

    The Bridge callback currently transports 16 positional values in the exact
    order defined by MCU_TELEMETRY_FIELDS. The validation is intentionally
    strict enough to catch schema drift without asserting hardware-derived
    values.
    """
    errors: list[str] = []

    if len(payload) != EXPECTED_CALLBACK_ARG_COUNT:
        errors.append(
            "Bridge payload must contain exactly "
            f"{EXPECTED_CALLBACK_ARG_COUNT} arguments; got {len(payload)}"
        )
        return errors

    mcu_timestamp_ms, speed_hall, speed_gps, latitude, longitude, gps_valid, \
        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, gyro_valid, \
        obstacle_distance, deterministic_alert, sensor_valid = payload

    if not _is_int_field(mcu_timestamp_ms):
        errors.append("mcu_timestamp_ms must be an integer")
    elif mcu_timestamp_ms < 0:
        errors.append("mcu_timestamp_ms cannot be negative")

    for name, value in (
        ("speed_hall", speed_hall),
        ("speed_gps", speed_gps),
        ("latitude", latitude),
        ("longitude", longitude),
        ("accel_x", accel_x),
        ("accel_y", accel_y),
        ("accel_z", accel_z),
        ("gyro_x", gyro_x),
        ("gyro_y", gyro_y),
        ("gyro_z", gyro_z),
        ("obstacle_distance", obstacle_distance),
    ):
        if not _is_finite_number(value):
            errors.append(f"{name} must be a finite numeric value")

    for name, value in (
        ("gps_valid", gps_valid),
        ("gyro_valid", gyro_valid),
        ("sensor_valid", sensor_valid),
    ):
        if not isinstance(value, bool):
            errors.append(f"{name} must be boolean")

    if not _is_int_field(deterministic_alert):
        errors.append("deterministic_alert must be an integer")
    elif deterministic_alert not in VALID_ALERT_IDS:
        errors.append(
            "deterministic_alert must be one of "
            f"{sorted(VALID_ALERT_IDS)}"
        )

    return errors

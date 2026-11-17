from __future__ import annotations

import math
from typing import Any

from firmware.linux.bridge_contract import OBSTACLE_DISTANCE_UNAVAILABLE


REQUIRED_FIELDS = [
	"timestamp",
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
	"obstacle_distance",
	"deterministic_alert",
	"sensor_valid",
]


def validate_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
	"""
	Validate one Smart Speed Guard telemetry record.

	Returns:
		(True, []) when the record is valid.
		(False, errors) when one or more validation checks fail.
	"""

	errors: list[str] = []

	# Check that all required fields exist.
	for field in REQUIRED_FIELDS:
		if field not in record:
			errors.append(f"Missing field: {field}")

	if errors:
		return False, errors

	# Timestamp must be numeric and non-negative.
	if not isinstance(record["timestamp"], (int, float)):
		errors.append("timestamp must be numeric")
	elif record["timestamp"] < 0:
		errors.append("timestamp cannot be negative")

	# Speed values must be numeric and non-negative.
	for field in ("speed_hall", "speed_gps"):
		value = record[field]

		if not isinstance(value, (int, float)):
			errors.append(f"{field} must be numeric")
		elif value < 0:
			errors.append(f"{field} cannot be negative")

	# GPS validity flag must be boolean.
	if not isinstance(record["gps_valid"], bool):
		errors.append("gps_valid must be boolean")

	# GPS coordinates are checked only when a valid GPS fix is reported.
	if record["gps_valid"]:
		latitude = record["latitude"]
		longitude = record["longitude"]

		if not isinstance(latitude, (int, float)):
			errors.append("latitude must be numeric")

		elif not -90 <= latitude <= 90:
			errors.append("latitude is outside valid range")

		if not isinstance(longitude, (int, float)):
			errors.append("longitude must be numeric")

		elif not -180 <= longitude <= 180:
			errors.append("longitude is outside valid range")

	# IMU values must be numeric.
	imu_fields = [
		"accel_x",
		"accel_y",
		"accel_z",
		"gyro_x",
		"gyro_y",
		"gyro_z",
	]

	for field in imu_fields:
		if not isinstance(record[field], (int, float)):
			errors.append(f"{field} must be numeric")

	# -1.0 is a transport sentinel, not a physical distance.
	distance = record["obstacle_distance"]

	if isinstance(distance, bool) or not isinstance(distance, (int, float)):
		errors.append("obstacle_distance must be numeric")
	elif not math.isfinite(float(distance)):
		errors.append("obstacle_distance must be finite")
	elif (
		distance < 0
		and distance != OBSTACLE_DISTANCE_UNAVAILABLE
	):
		errors.append("obstacle_distance cannot be negative")

	# Deterministic alert state must be an integer.
	if not isinstance(record["deterministic_alert"], int):
		errors.append("deterministic_alert must be an integer")

	# sensor_valid reports accelerometer validity only.
	if not isinstance(record["sensor_valid"], bool):
		errors.append("sensor_valid must be boolean")

	return len(errors) == 0, errors


if __name__ == "__main__":
	print("Smart Speed Guard telemetry validator")
	print("Validator module loaded successfully.")

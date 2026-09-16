from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def load_real_accelerometer_csv(
	csv_path: str | Path,
) -> list[dict[str, Any]]:
	"""
	Load the currently available real UNO Q telemetry CSV.

	The current hardware telemetry contains only:
		timestamp_ms, accel_x, accel_y, accel_z, sensor_valid

	Other project telemetry fields are explicitly marked as unavailable
	rather than being populated with fabricated measurements.
	"""

	path = Path(csv_path)

	if not path.exists():
		raise FileNotFoundError(f"Telemetry CSV not found: {path}")

	records: list[dict[str, Any]] = []

	with path.open("r", newline="") as file:
		reader = csv.DictReader(file)

		required_columns = {
			"timestamp_ms",
			"accel_x",
			"accel_y",
			"accel_z",
			"sensor_valid",
		}

		missing_columns = required_columns - set(reader.fieldnames or [])

		if missing_columns:
			raise ValueError(
				f"Missing required CSV columns: {sorted(missing_columns)}"
			)

		for row in reader:
			sensor_valid = row["sensor_valid"].strip().lower() == "true"

			record = {
				"timestamp": int(row["timestamp_ms"]),
				"speed_hall": 0.0,
				"speed_gps": 0.0,
				"latitude": 0.0,
				"longitude": 0.0,
				"gps_valid": False,
				"accel_x": float(row["accel_x"]),
				"accel_y": float(row["accel_y"]),
				"accel_z": float(row["accel_z"]),
				"gyro_x": 0.0,
				"gyro_y": 0.0,
				"gyro_z": 0.0,
				"obstacle_distance": 0.0,
				"deterministic_alert": 0,
				"sensor_valid": sensor_valid,
			}

			records.append(record)

	return records

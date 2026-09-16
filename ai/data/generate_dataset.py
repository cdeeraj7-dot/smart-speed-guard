from __future__ import annotations

import csv
import random
from pathlib import Path


FIELDNAMES = [
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


def generate_record(timestamp: int) -> dict:
	"""Generate one synthetic telemetry record for pipeline testing."""

	speed = 40.0 + random.uniform(-2.0, 2.0)

	return {
		"timestamp": timestamp,
		"speed_hall": round(speed, 2),
		"speed_gps": round(speed + random.uniform(-1.0, 1.0), 2),
		"latitude": round(12.9716 + random.uniform(-0.0001, 0.0001), 6),
		"longitude": round(77.5946 + random.uniform(-0.0001, 0.0001), 6),
		"gps_valid": True,
		"accel_x": round(random.uniform(-0.3, 0.3), 3),
		"accel_y": round(random.uniform(-0.3, 0.3), 3),
		"accel_z": round(9.8 + random.uniform(-0.2, 0.2), 3),
		"gyro_x": round(random.uniform(-1.0, 1.0), 3),
		"gyro_y": round(random.uniform(-1.0, 1.0), 3),
		"gyro_z": round(random.uniform(-1.0, 1.0), 3),
		"obstacle_distance": round(random.uniform(100.0, 200.0), 2),
		"deterministic_alert": 0,
		"sensor_valid": True,
	}


def generate_dataset(
	output_path: str | Path,
	num_records: int = 1000,
	sample_interval_ms: int = 100,
) -> Path:
	"""Generate synthetic telemetry and save it as CSV."""

	if num_records <= 0:
		raise ValueError("num_records must be greater than zero")

	if sample_interval_ms <= 0:
		raise ValueError("sample_interval_ms must be greater than zero")

	output = Path(output_path)
	output.parent.mkdir(parents=True, exist_ok=True)

	random.seed(42)

	records = [
		generate_record(index * sample_interval_ms)
		for index in range(num_records)
	]

	with output.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
		writer.writeheader()
		writer.writerows(records)

	return output


if __name__ == "__main__":
	output_file = generate_dataset(
		Path(__file__).parent / "raw" / "synthetic_telemetry.csv"
	)

	print(f"Generated synthetic telemetry: {output_file}")

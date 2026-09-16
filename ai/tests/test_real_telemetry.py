from pathlib import Path

from ai.preprocessing.real_telemetry import load_real_accelerometer_csv


def test_load_real_accelerometer_csv(tmp_path: Path):
	csv_file = tmp_path / "telemetry.csv"

	csv_file.write_text(
		"timestamp_ms,accel_x,accel_y,accel_z,sensor_valid\n"
		"1000,0.1,0.2,0.9,True\n"
		"1500,-0.1,0.3,1.0,True\n"
	)

	records = load_real_accelerometer_csv(csv_file)

	assert len(records) == 2

	assert records[0]["timestamp"] == 1000
	assert records[0]["accel_x"] == 0.1
	assert records[0]["accel_y"] == 0.2
	assert records[0]["accel_z"] == 0.9
	assert records[0]["sensor_valid"] is True

	assert records[0]["gps_valid"] is False
	assert records[0]["speed_hall"] == 0.0
	assert records[0]["speed_gps"] == 0.0
	assert records[0]["obstacle_distance"] == 0.0


def test_missing_required_column(tmp_path: Path):
	csv_file = tmp_path / "telemetry.csv"

	csv_file.write_text(
		"timestamp_ms,accel_x,accel_y,accel_z\n"
		"1000,0.1,0.2,0.9\n"
	)

	try:
		load_real_accelerometer_csv(csv_file)
		assert False, "Expected ValueError"
	except ValueError as error:
		assert "sensor_valid" in str(error)

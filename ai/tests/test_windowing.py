from ai.preprocessing.windowing import create_windows


def make_record(timestamp):
	return {
		"timestamp": timestamp,
		"speed_hall": 40.0,
		"speed_gps": 39.5,
		"latitude": 12.9716,
		"longitude": 77.5946,
		"gps_valid": True,
		"accel_x": 0.1,
		"accel_y": 0.2,
		"accel_z": 9.8,
		"gyro_x": 0.5,
		"gyro_y": 0.3,
		"gyro_z": 0.2,
		"obstacle_distance": 150.0,
		"deterministic_alert": 0,
		"sensor_valid": True,
	}


def test_empty_records():
	assert create_windows([]) == []


def test_records_are_sorted_by_timestamp():
	records = [
		make_record(4000),
		make_record(1000),
		make_record(2000),
	]

	windows = create_windows(
		records,
		window_ms=5000,
		overlap=0,
		min_samples=1,
	)

	assert [record["timestamp"] for record in windows[0]] == [
		1000,
		2000,
		4000,
	]


def test_window_groups_records_by_time():
	records = [
		make_record(0),
		make_record(1000),
		make_record(3000),
		make_record(6000),
	]

	windows = create_windows(
		records,
		window_ms=5000,
		overlap=0,
		min_samples=1,
	)

	assert len(windows) == 2
	assert len(windows[0]) == 3
	assert len(windows[1]) == 1


def test_minimum_samples():
	records = [
		make_record(0),
		make_record(1000),
	]

	windows = create_windows(
		records,
		window_ms=5000,
		overlap=0,
		min_samples=3,
	)

	assert windows == []


def test_invalid_window_parameters():
	records = [make_record(0)]

	try:
		create_windows(records, window_ms=0)
		assert False
	except ValueError:
		pass

	try:
		create_windows(records, overlap=1.0)
		assert False
	except ValueError:
		pass

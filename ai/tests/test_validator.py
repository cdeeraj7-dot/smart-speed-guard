from ai.preprocessing.validator import validate_record

def valid_record():
	return {
		"timestamp": 1000,
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


def test_valid_record():
	record = valid_record()

	is_valid, errors = validate_record(record)

	assert is_valid is True
	assert errors == []


def test_missing_field():
	record = valid_record()
	del record["speed_hall"]

	is_valid, errors = validate_record(record)

	assert is_valid is False
	assert "Missing field: speed_hall" in errors


def test_negative_speed():
	record = valid_record()
	record["speed_hall"] = -10.0

	is_valid, errors = validate_record(record)

	assert is_valid is False
	assert "speed_hall cannot be negative" in errors


def test_invalid_gps_coordinates():
	record = valid_record()
	record["latitude"] = 100.0

	is_valid, errors = validate_record(record)

	assert is_valid is False
	assert "latitude is outside valid range" in errors


def test_invalid_sensor_status():
	record = valid_record()
	record["sensor_valid"] = False

	is_valid, errors = validate_record(record)

	assert is_valid is False
	assert "sensor_valid is false" in errors

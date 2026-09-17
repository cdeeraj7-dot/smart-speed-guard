import math

from ai.features import extractor
from ai.features.extractor import extract_features


def make_record(
	timestamp,
	speed_hall=40.0,
	speed_gps=39.5,
	gps_valid=True,
	accel_x=0.0,
	accel_y=0.0,
	accel_z=9.8,
	gyro_x=0.0,
	gyro_y=0.0,
	gyro_z=0.0,
	obstacle_distance=150.0,
	deterministic_alert=0,
	sensor_valid=True,
):
	return {
		"timestamp": timestamp,
		"speed_hall": speed_hall,
		"speed_gps": speed_gps,
		"latitude": 12.9716,
		"longitude": 77.5946,
		"gps_valid": gps_valid,
		"accel_x": accel_x,
		"accel_y": accel_y,
		"accel_z": accel_z,
		"gyro_x": gyro_x,
		"gyro_y": gyro_y,
		"gyro_z": gyro_z,
		"obstacle_distance": obstacle_distance,
		"deterministic_alert": deterministic_alert,
		"sensor_valid": sensor_valid,
	}


def test_empty_window_rejected():
	try:
		extract_features([])
		assert False
	except ValueError:
		pass


def test_speed_features():
	window = [
		make_record(0, speed_hall=20.0),
		make_record(1000, speed_hall=40.0),
		make_record(2000, speed_hall=60.0),
	]

	features = extract_features(window)

	assert features["speed_hall_mean"] == 40.0
	assert features["speed_hall_min"] == 20.0
	assert features["speed_hall_max"] == 60.0


def test_acceleration_magnitude():
	window = [
		make_record(
			0,
			accel_x=3.0,
			accel_y=4.0,
			accel_z=0.0,
		)
	]

	features = extract_features(window)

	assert features["accel_magnitude_mean"] == 5.0
	assert features["accel_magnitude_max"] == 5.0


def test_gyro_magnitude():
	window = [
		make_record(
			0,
			gyro_x=3.0,
			gyro_y=4.0,
			gyro_z=0.0,
		)
	]

	features = extract_features(window)

	assert features["gyro_magnitude_mean"] == 5.0
	assert features["gyro_magnitude_max"] == 5.0


def test_obstacle_distance_features():
	window = [
		make_record(0, obstacle_distance=100.0),
		make_record(1000, obstacle_distance=200.0),
		make_record(2000, obstacle_distance=300.0),
	]

	features = extract_features(window)

	assert features["obstacle_distance_mean"] == 200.0
	assert features["obstacle_distance_min"] == 100.0


def test_alert_count():
	window = [
		make_record(0, deterministic_alert=0),
		make_record(1000, deterministic_alert=1),
		make_record(2000, deterministic_alert=2),
	]

	features = extract_features(window)

	assert features["deterministic_alert_count"] == 2.0


def test_sensor_valid_percentage():
	window = [
		make_record(0, sensor_valid=True),
		make_record(1000, sensor_valid=True),
		make_record(2000, sensor_valid=False),
		make_record(3000, sensor_valid=False),
	]

	features = extract_features(window)

	assert math.isclose(
		features["sensor_valid_percentage"],
		0.5,
	)


def test_gps_valid_percentage_and_mean():
	window = [
		make_record(
			0,
			speed_gps=40.0,
			gps_valid=True,
		),
		make_record(
			1000,
			speed_gps=50.0,
			gps_valid=True,
		),
		make_record(
			2000,
			speed_gps=0.0,
			gps_valid=False,
		),
	]

	features = extract_features(window)

	assert features["speed_gps_mean"] == 45.0

	assert math.isclose(
		features["gps_valid_percentage"],
		2 / 3,
	)


def test_available_sensor_features():
	window = [
		make_record(
			0,
			accel_x=1.0,
			accel_y=0.0,
			accel_z=0.0,
			sensor_valid=True,
		),
		make_record(
			1000,
			accel_x=0.0,
			accel_y=1.0,
			accel_z=0.0,
			sensor_valid=True,
		),
	]

	features = extractor.extract_available_sensor_features(window)

	assert "accel_magnitude_mean" in features
	assert "accel_magnitude_max" in features
	assert "accel_magnitude_std" in features
	assert "sensor_valid_percentage" in features

	assert features["accel_magnitude_mean"] == 1.0
	assert features["accel_magnitude_max"] == 1.0
	assert features["sensor_valid_percentage"] == 1.0


def test_available_sensor_features_do_not_fabricate_unavailable_sensors():
	window = [
		make_record(
			0,
			accel_x=1.0,
			accel_y=0.0,
			accel_z=0.0,
			sensor_valid=True,
		),
	]

	features = extractor.extract_available_sensor_features(window)

	assert "speed_hall_mean" not in features
	assert "speed_gps_mean" not in features
	assert "gyro_magnitude_mean" not in features
	assert "obstacle_distance_mean" not in features

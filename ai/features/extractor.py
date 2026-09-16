from __future__ import annotations

import math
from typing import Any


def _mean(values: list[float]) -> float:
	return sum(values) / len(values)


def _std(values: list[float]) -> float:
	if len(values) < 2:
		return 0.0

	mean = _mean(values)
	variance = sum((value - mean) ** 2 for value in values) / len(values)

	return math.sqrt(variance)


def _acceleration_magnitude(record: dict[str, Any]) -> float:
	return math.sqrt(
		record["accel_x"] ** 2
		+ record["accel_y"] ** 2
		+ record["accel_z"] ** 2
	)


def _gyroscope_magnitude(record: dict[str, Any]) -> float:
	return math.sqrt(
		record["gyro_x"] ** 2
		+ record["gyro_y"] ** 2
		+ record["gyro_z"] ** 2
	)


def extract_features(window: list[dict[str, Any]]) -> dict[str, float]:
	"""
	Convert one validated telemetry window into an ML-ready feature vector.
	"""

	if not window:
		raise ValueError("Cannot extract features from an empty window")

	hall_speeds = [record["speed_hall"] for record in window]

	valid_gps_speeds = [
		record["speed_gps"]
		for record in window
		if record["gps_valid"]
	]

	acceleration_magnitudes = [
		_acceleration_magnitude(record)
		for record in window
	]

	gyroscope_magnitudes = [
		_gyroscope_magnitude(record)
		for record in window
	]

	obstacle_distances = [
		record["obstacle_distance"]
		for record in window
	]

	deterministic_alert_count = sum(
		1
		for record in window
		if record["deterministic_alert"] != 0
	)

	sensor_valid_count = sum(
		1
		for record in window
		if record["sensor_valid"]
	)

	gps_valid_count = sum(
		1
		for record in window
		if record["gps_valid"]
	)

	sample_count = len(window)

	features = {
		"speed_hall_mean": _mean(hall_speeds),
		"speed_hall_max": max(hall_speeds),
		"speed_hall_min": min(hall_speeds),
		"speed_hall_std": _std(hall_speeds),

		"speed_gps_mean": (
			_mean(valid_gps_speeds)
			if valid_gps_speeds
			else 0.0
		),

		"accel_magnitude_mean": _mean(acceleration_magnitudes),
		"accel_magnitude_max": max(acceleration_magnitudes),
		"accel_magnitude_std": _std(acceleration_magnitudes),

		"gyro_magnitude_mean": _mean(gyroscope_magnitudes),
		"gyro_magnitude_max": max(gyroscope_magnitudes),
		"gyro_magnitude_std": _std(gyroscope_magnitudes),

		"obstacle_distance_mean": _mean(obstacle_distances),
		"obstacle_distance_min": min(obstacle_distances),
		"obstacle_distance_std": _std(obstacle_distances),

		"deterministic_alert_count": float(
			deterministic_alert_count
		),

		"sensor_valid_percentage": (
			sensor_valid_count / sample_count
		),

		"gps_valid_percentage": (
			gps_valid_count / sample_count
		),
	}

	return features

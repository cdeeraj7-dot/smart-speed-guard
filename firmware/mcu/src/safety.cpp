#include "safety.h"

#include <cmath>

#include "obstacle_state.h"

namespace {

// These are provisional development defaults only. They must be replaced with
// measured, bench-tested thresholds before any field deployment or safety claim.
constexpr float OVERSPEED_TRIGGER = 120.0f;
constexpr float OVERSPEED_RELEASE = 105.0f;
constexpr float OBSTACLE_TRIGGER = 6.0f;
constexpr float OBSTACLE_RELEASE = 8.0f;
constexpr float IMPACT_TRIGGER = 2.5f;
constexpr float IMPACT_RELEASE = 2.0f;

bool isFinite(float value) {
	return std::isfinite(value);
}

AlertType chooseAlert(
	float speed_hall,
	float obstacle_distance,
	bool obstacle_valid,
	float acceleration_magnitude,
	bool acceleration_valid,
	AlertType previous_alert
) {
	if (previous_alert == AlertType::IMPACT && !acceleration_valid) {
		return AlertType::IMPACT;
	}

	if (acceleration_valid &&
		isFinite(acceleration_magnitude) &&
		acceleration_magnitude >= IMPACT_TRIGGER) {
		return AlertType::IMPACT;
	}

	if (obstacle_valid &&
		isFinite(obstacle_distance) &&
		obstacle_distance <= OBSTACLE_TRIGGER) {
		return AlertType::OBSTACLE;
	}

	if (isFinite(speed_hall) &&
		speed_hall >= OVERSPEED_TRIGGER) {
		return AlertType::OVERSPEED;
	}

	if (previous_alert == AlertType::IMPACT &&
		acceleration_valid &&
		isFinite(acceleration_magnitude) &&
		acceleration_magnitude <= IMPACT_RELEASE) {
		return AlertType::NONE;
	}

	if (previous_alert == AlertType::OBSTACLE &&
		obstacle_valid &&
		isFinite(obstacle_distance) &&
		obstacle_distance >= OBSTACLE_RELEASE) {
		return AlertType::NONE;
	}

	if (previous_alert == AlertType::OVERSPEED &&
		isFinite(speed_hall) &&
		speed_hall <= OVERSPEED_RELEASE) {
		return AlertType::NONE;
	}

	return previous_alert;
}

}  // namespace

SafetyStatus evaluateSafety(
	float speed_hall,
	float obstacle_distance,
	float acceleration_magnitude,
	bool acceleration_valid
) {
	const bool obstacle_valid =
		isFinite(obstacle_distance) &&
		obstacle_distance >= 0.0f &&
		obstacle_distance != OBSTACLE_DISTANCE_UNAVAILABLE;

	return evaluateSafety(
		speed_hall,
		obstacle_distance,
		acceleration_magnitude,
		acceleration_valid,
		obstacle_valid
	);
}

SafetyStatus evaluateSafety(
	float speed_hall,
	float obstacle_distance,
	float acceleration_magnitude,
	bool acceleration_valid,
	bool obstacle_valid
) {
	static AlertType previous_alert = AlertType::NONE;
	static bool obstacle_alert_latched = false;

	if (!isFinite(speed_hall)) {
		speed_hall = 0.0f;
	}

	if (!isFinite(obstacle_distance) ||
		obstacle_distance < 0.0f ||
		obstacle_distance == OBSTACLE_DISTANCE_UNAVAILABLE) {
		obstacle_valid = false;
	}

	if (obstacle_valid) {
		if (obstacle_distance <= OBSTACLE_TRIGGER) {
			obstacle_alert_latched = true;
		} else if (obstacle_distance >= OBSTACLE_RELEASE) {
			obstacle_alert_latched = false;
		}
	}

	if (!isFinite(acceleration_magnitude)) {
		acceleration_valid = false;
	}

	AlertType next_alert = chooseAlert(
		speed_hall,
		obstacle_distance,
		obstacle_valid,
		acceleration_magnitude,
		acceleration_valid,
		previous_alert
	);

	if (next_alert == AlertType::NONE &&
		speed_hall >= OVERSPEED_TRIGGER) {
		next_alert = AlertType::OVERSPEED;
	}

	if (next_alert == AlertType::NONE &&
		obstacle_valid &&
		obstacle_distance <= OBSTACLE_TRIGGER) {
		next_alert = AlertType::OBSTACLE;
	}

	if (next_alert == AlertType::NONE &&
		acceleration_valid &&
		isFinite(acceleration_magnitude) &&
		acceleration_magnitude >= IMPACT_TRIGGER) {
		next_alert = AlertType::IMPACT;
	}

	if (next_alert == AlertType::NONE && obstacle_alert_latched) {
		next_alert = AlertType::OBSTACLE;
	}

	previous_alert = next_alert;

	SafetyStatus status;
	status.alert = next_alert;
	status.buzzer_active = next_alert != AlertType::NONE;
	status.led_active = next_alert != AlertType::NONE;

	return status;
}

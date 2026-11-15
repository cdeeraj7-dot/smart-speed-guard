#include "safety.h"

#include <cmath>

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
	float acceleration_magnitude,
	AlertType previous_alert
) {
	if (isFinite(acceleration_magnitude) &&
		acceleration_magnitude >= IMPACT_TRIGGER) {
		return AlertType::IMPACT;
	}

	if (isFinite(obstacle_distance) &&
		obstacle_distance <= OBSTACLE_TRIGGER) {
		return AlertType::OBSTACLE;
	}

	if (isFinite(speed_hall) &&
		speed_hall >= OVERSPEED_TRIGGER) {
		return AlertType::OVERSPEED;
	}

	if (previous_alert == AlertType::IMPACT &&
		isFinite(acceleration_magnitude) &&
		acceleration_magnitude <= IMPACT_RELEASE) {
		return AlertType::NONE;
	}

	if (previous_alert == AlertType::OBSTACLE &&
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
	float acceleration_magnitude
) {
	static AlertType previous_alert = AlertType::NONE;

	if (!isFinite(speed_hall)) {
		speed_hall = 0.0f;
	}

	if (!isFinite(obstacle_distance)) {
		obstacle_distance = 0.0f;
	}

	if (!isFinite(acceleration_magnitude)) {
		acceleration_magnitude = 0.0f;
	}

	AlertType next_alert = chooseAlert(
		speed_hall,
		obstacle_distance,
		acceleration_magnitude,
		previous_alert
	);

	if (next_alert == AlertType::NONE &&
		speed_hall >= OVERSPEED_TRIGGER) {
		next_alert = AlertType::OVERSPEED;
	}

	if (next_alert == AlertType::NONE &&
		obstacle_distance <= OBSTACLE_TRIGGER) {
		next_alert = AlertType::OBSTACLE;
	}

	if (next_alert == AlertType::NONE &&
		acceleration_magnitude >= IMPACT_TRIGGER) {
		next_alert = AlertType::IMPACT;
	}

	previous_alert = next_alert;

	SafetyStatus status;
	status.alert = next_alert;
	status.buzzer_active = next_alert != AlertType::NONE;
	status.led_active = next_alert != AlertType::NONE;

	return status;
}

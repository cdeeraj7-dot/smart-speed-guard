#include "safety.h"

SafetyStatus evaluateSafety(
	float speed_hall,
	float obstacle_distance,
	float acceleration_magnitude
) {
	// Safety thresholds are intentionally not defined yet.
	// They must be determined and validated during Phase 2 testing.

	(void)speed_hall;
	(void)obstacle_distance;
	(void)acceleration_magnitude;

	SafetyStatus status;

	status.alert = AlertType::NONE;
	status.buzzer_active = false;
	status.led_active = false;

	return status;
}

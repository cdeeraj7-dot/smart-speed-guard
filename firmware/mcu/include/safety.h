#ifndef SMART_SPEED_GUARD_SAFETY_H
#define SMART_SPEED_GUARD_SAFETY_H

#include <stdint.h>

enum class AlertType : uint8_t {
	NONE = 0,
	OVERSPEED = 1,
	OBSTACLE = 2,
	IMPACT = 3
};

struct SafetyStatus {
	AlertType alert;
	bool buzzer_active;
	bool led_active;
};

SafetyStatus evaluateSafety(
	float speed_hall,
	float obstacle_distance,
	float acceleration_magnitude
);

#endif

#ifndef SMART_SPEED_GUARD_OBSTACLE_STATE_H
#define SMART_SPEED_GUARD_OBSTACLE_STATE_H

#include <stdint.h>

constexpr float OBSTACLE_DISTANCE_UNAVAILABLE = -1.0f;

struct ObstacleReading {
	float distance_cm;
	bool valid;
};

class ObstacleValidityTracker {
public:
	static constexpr uint8_t RECOVERY_SAMPLES_REQUIRED = 2;

	ObstacleValidityTracker();

	bool observe(
		float distance_cm,
		bool acquisition_succeeded,
		uint32_t sample_time_ms,
		uint32_t freshness_timeout_ms
	);
	ObstacleReading current(uint32_t now_ms);
	void markUnavailable();

private:
	float distance_cm_;
	uint32_t sample_time_ms_;
	uint32_t freshness_timeout_ms_;
	uint8_t recovery_samples_;
	bool has_sample_;
};

#endif

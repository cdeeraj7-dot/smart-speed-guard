#include "obstacle_state.h"

#include <cmath>

ObstacleValidityTracker::ObstacleValidityTracker()
	: distance_cm_(OBSTACLE_DISTANCE_UNAVAILABLE),
	  sample_time_ms_(0),
	  freshness_timeout_ms_(0),
	  recovery_samples_(0),
	  has_sample_(false) {
}

bool ObstacleValidityTracker::observe(
	float distance_cm,
	bool acquisition_succeeded,
	uint32_t sample_time_ms,
	uint32_t freshness_timeout_ms
) {
	if (!acquisition_succeeded ||
		!std::isfinite(distance_cm) ||
		distance_cm < 0.0f ||
		freshness_timeout_ms == 0) {
		markUnavailable();
		return false;
	}

	if (has_sample_ &&
		sample_time_ms - sample_time_ms_ > freshness_timeout_ms_) {
		recovery_samples_ = 0;
	}

	distance_cm_ = distance_cm;
	sample_time_ms_ = sample_time_ms;
	freshness_timeout_ms_ = freshness_timeout_ms;
	has_sample_ = true;

	if (recovery_samples_ < RECOVERY_SAMPLES_REQUIRED) {
		++recovery_samples_;
	}

	return recovery_samples_ >= RECOVERY_SAMPLES_REQUIRED;
}

ObstacleReading ObstacleValidityTracker::current(uint32_t now_ms) {
	if (!has_sample_ ||
		now_ms - sample_time_ms_ > freshness_timeout_ms_) {
		markUnavailable();
		return {OBSTACLE_DISTANCE_UNAVAILABLE, false};
	}

	if (recovery_samples_ < RECOVERY_SAMPLES_REQUIRED) {
		return {OBSTACLE_DISTANCE_UNAVAILABLE, false};
	}

	return {distance_cm_, true};
}

void ObstacleValidityTracker::markUnavailable() {
	distance_cm_ = OBSTACLE_DISTANCE_UNAVAILABLE;
	sample_time_ms_ = 0;
	freshness_timeout_ms_ = 0;
	recovery_samples_ = 0;
	has_sample_ = false;
}

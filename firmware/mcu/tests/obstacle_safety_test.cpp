#include <assert.h>
#include <math.h>

#include "../include/obstacle_state.h"
#include "../include/safety.h"
#include "../include/telemetry.h"
#include "../src/obstacle_state.cpp"
#include "../src/safety.cpp"
#include "../src/telemetry.cpp"

void runObstacleSafetyTests() {
	TelemetryData telemetry;
	initializeTelemetry(telemetry);
	assert(telemetry.obstacle_distance == OBSTACLE_DISTANCE_UNAVAILABLE);
	assert(!telemetry.obstacle_valid);

	ObstacleValidityTracker tracker;
	ObstacleReading reading = tracker.current(0);
	assert(!reading.valid);
	assert(reading.distance_cm == OBSTACLE_DISTANCE_UNAVAILABLE);

	SafetyStatus status = evaluateSafety(
		0.0f,
		reading.distance_cm,
		0.0f,
		false,
		reading.valid
	);
	assert(status.alert == AlertType::NONE);

	assert(!tracker.observe(5.0f, true, 10, 50));
	reading = tracker.current(10);
	assert(!reading.valid);
	assert(reading.distance_cm == OBSTACLE_DISTANCE_UNAVAILABLE);
	assert(tracker.observe(5.0f, true, 20, 50));

	reading = tracker.current(20);
	assert(reading.valid);
	assert(reading.distance_cm == 5.0f);
	status = evaluateSafety(0.0f, reading.distance_cm, 0.0f, false, reading.valid);
	assert(status.alert == AlertType::OBSTACLE);

	tracker.markUnavailable();
	reading = tracker.current(21);
	assert(!reading.valid);
	status = evaluateSafety(0.0f, reading.distance_cm, 0.0f, false, reading.valid);
	assert(status.alert == AlertType::OBSTACLE);

	status = evaluateSafety(130.0f, reading.distance_cm, 0.0f, false, reading.valid);
	assert(status.alert == AlertType::OVERSPEED);
	status = evaluateSafety(0.0f, reading.distance_cm, 0.0f, false, reading.valid);
	assert(status.alert == AlertType::OBSTACLE);

	assert(!tracker.observe(10.0f, true, 30, 50));
	assert(tracker.observe(10.0f, true, 40, 50));
	reading = tracker.current(40);
	assert(reading.valid);
	status = evaluateSafety(0.0f, reading.distance_cm, 0.0f, false, reading.valid);
	assert(status.alert == AlertType::NONE);
	reading = tracker.current(91);
	assert(!reading.valid);
	assert(reading.distance_cm == OBSTACLE_DISTANCE_UNAVAILABLE);

	assert(!tracker.observe(NAN, true, 50, 50));
	assert(!tracker.current(50).valid);
	assert(!tracker.observe(-2.0f, true, 60, 50));
	assert(!tracker.current(60).valid);

	assert(!tracker.observe(5.0f, true, 70, 50));
	assert(!tracker.current(70).valid);
	assert(!tracker.observe(5.0f, false, 80, 50));
	assert(!tracker.current(80).valid);

	assert(!tracker.observe(10.0f, true, 90, 50));
	assert(!tracker.observe(10.0f, true, 151, 50));
	assert(!tracker.current(151).valid);
	assert(!tracker.observe(10.0f, true, 160, 50));
	assert(tracker.observe(10.0f, true, 170, 50));
	reading = tracker.current(170);
	assert(reading.valid);

	status = evaluateSafety(
		130.0f,
		reading.distance_cm,
		3.0f,
		true,
		reading.valid
	);
	assert(status.alert == AlertType::IMPACT);

	tracker.markUnavailable();
	reading = tracker.current(171);
	status = evaluateSafety(
		0.0f,
		reading.distance_cm,
		NAN,
		false,
		reading.valid
	);
	assert(status.alert == AlertType::IMPACT);

	status = evaluateSafety(
		0.0f,
		reading.distance_cm,
		0.0f,
		true,
		reading.valid
	);
	assert(status.alert == AlertType::NONE);

	status = evaluateSafety(
		130.0f,
		reading.distance_cm,
		0.0f,
		true,
		reading.valid
	);
	assert(status.alert == AlertType::OVERSPEED);
}

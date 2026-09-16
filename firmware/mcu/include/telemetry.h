#ifndef SMART_SPEED_GUARD_TELEMETRY_H
#define SMART_SPEED_GUARD_TELEMETRY_H

#include <stdint.h>

struct TelemetryData {
	uint64_t timestamp;

	float speed_hall;
	float speed_gps;

	float latitude;
	float longitude;

	bool gps_valid;

	float accel_x;
	float accel_y;
	float accel_z;

	float gyro_x;
	float gyro_y;
	float gyro_z;

	float obstacle_distance;

	uint8_t deterministic_alert;

	bool sensor_valid;
};
void initializeTelemetry(TelemetryData& telemetry);

#endif

#include "telemetry.h"

void initializeTelemetry(TelemetryData& telemetry) {
	telemetry.timestamp = 0;

	telemetry.speed_hall = 0.0f;
	telemetry.speed_gps = 0.0f;

	telemetry.latitude = 0.0f;
	telemetry.longitude = 0.0f;

	telemetry.gps_valid = false;

	telemetry.accel_x = 0.0f;
	telemetry.accel_y = 0.0f;
	telemetry.accel_z = 0.0f;

	telemetry.gyro_x = 0.0f;
	telemetry.gyro_y = 0.0f;
	telemetry.gyro_z = 0.0f;

	telemetry.obstacle_distance = 0.0f;

	telemetry.deterministic_alert = 0;

	telemetry.sensor_valid = false;
}

#ifndef SMART_SPEED_GUARD_IMU_H
#define SMART_SPEED_GUARD_IMU_H

#include <stdint.h>

struct IMUData {
	float accel_x;
	float accel_y;
	float accel_z;

	bool accel_valid;

	// Gyroscope is currently unavailable because
	// the Z-axis output of the present MPU6050 module
	// is not behaving correctly.
	float gyro_x;
	float gyro_y;
	float gyro_z;

	bool gyro_valid;
};

bool initializeIMU();

bool readIMU(IMUData& data);

#endif

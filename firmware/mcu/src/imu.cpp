#include "imu.h"

#include <Arduino.h>
#include <Wire.h>

namespace {

constexpr uint8_t MPU6050_ADDRESS = 0x68;

constexpr uint8_t REG_PWR_MGMT_1 = 0x6B;
constexpr uint8_t REG_ACCEL_CONFIG = 0x1C;
constexpr uint8_t REG_ACCEL_XOUT_H = 0x3B;

constexpr float ACCEL_SCALE = 16384.0f;

bool imu_initialized = false;

bool writeRegister(uint8_t reg, uint8_t value) {
	Wire2.beginTransmission(MPU6050_ADDRESS);
	Wire2.write(reg);
	Wire2.write(value);

	return Wire2.endTransmission() == 0;
}

bool readRegisters(uint8_t start_register, uint8_t* buffer, uint8_t length) {
	Wire2.beginTransmission(MPU6050_ADDRESS);
	Wire2.write(start_register);

	if (Wire2.endTransmission(false) != 0) {
		return false;
	}

	uint8_t received = Wire2.requestFrom(
		MPU6050_ADDRESS,
		length
	);

	if (received != length) {
		return false;
	}

	for (uint8_t i = 0; i < length; ++i) {
		if (!Wire2.available()) {
			return false;
		}

		buffer[i] = Wire2.read();
	}

	return true;
}

int16_t combineBytes(uint8_t high_byte, uint8_t low_byte) {
	return static_cast<int16_t>(
		(static_cast<uint16_t>(high_byte) << 8) |
		static_cast<uint16_t>(low_byte)
	);
}

}  // namespace

bool initializeIMU() {
	Wire2.begin();

	// Wake up the MPU6050.
	if (!writeRegister(REG_PWR_MGMT_1, 0x00)) {
		imu_initialized = false;
		return false;
	}

	// Accelerometer full-scale range = +/-2g.
	// At this setting the sensitivity is 16384 LSB/g.
	if (!writeRegister(REG_ACCEL_CONFIG, 0x00)) {
		imu_initialized = false;
		return false;
	}

	delay(100);

	imu_initialized = true;
	return true;
}

bool readIMU(IMUData& data) {
	data.accel_x = 0.0f;
	data.accel_y = 0.0f;
	data.accel_z = 0.0f;

	data.gyro_x = 0.0f;
	data.gyro_y = 0.0f;
	data.gyro_z = 0.0f;

	data.accel_valid = false;
	data.gyro_valid = false;

	if (!imu_initialized) {
		return false;
	}

	uint8_t buffer[6];

	if (!readRegisters(REG_ACCEL_XOUT_H, buffer, 6)) {
		return false;
	}

	int16_t raw_accel_x = combineBytes(buffer[0], buffer[1]);
	int16_t raw_accel_y = combineBytes(buffer[2], buffer[3]);
	int16_t raw_accel_z = combineBytes(buffer[4], buffer[5]);

	data.accel_x =
		static_cast<float>(raw_accel_x) / ACCEL_SCALE;

	data.accel_y =
		static_cast<float>(raw_accel_y) / ACCEL_SCALE;

	data.accel_z =
		static_cast<float>(raw_accel_z) / ACCEL_SCALE;

	data.accel_valid = true;

	// Gyroscope deliberately disabled for now.
	// The current MPU6050 module has an invalid Z-axis output.
	data.gyro_valid = false;

	return true;
}

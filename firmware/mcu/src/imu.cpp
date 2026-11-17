#include "imu.h"

#include <Arduino.h>
#include <Wire.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/i2c.h>

namespace {

constexpr uint8_t MPU6050_ADDRESS = 0x68;
constexpr uint8_t MPU6050_ALTERNATE_ADDRESS = 0x69;

constexpr uint8_t REG_PWR_MGMT_1 = 0x6B;
constexpr uint8_t REG_ACCEL_CONFIG = 0x1C;
constexpr uint8_t REG_ACCEL_XOUT_H = 0x3B;
constexpr uint8_t REG_WHO_AM_I = 0x75;
constexpr uint8_t MPU6050_WHO_AM_I = 0x68;

constexpr float ACCEL_SCALE = 16384.0f;

const struct device* const imu_i2c = DEVICE_DT_GET(DT_NODELABEL(i2c3));

bool imu_initialized = false;
bool read_error_reported = false;
uint8_t imu_address = 0;

void reportI2CFailure(const char* operation, int error) {
	Serial.print("MPU6050 ");
	Serial.print(operation);
	Serial.print(" failed; I2C error ");
	Serial.println(error);
}

int writeRegister(uint8_t reg, uint8_t value) {
	const uint8_t data[] = {reg, value};

	return i2c_write(imu_i2c, data, sizeof(data), imu_address);
}

int readRegisters(uint8_t address, uint8_t start_register, uint8_t* buffer, size_t length) {
	return i2c_write_read(
		imu_i2c,
		address,
		&start_register,
		sizeof(start_register),
		buffer,
		length
	);
}

int16_t combineBytes(uint8_t high_byte, uint8_t low_byte) {
	return static_cast<int16_t>(
		(static_cast<uint16_t>(high_byte) << 8) |
		static_cast<uint16_t>(low_byte)
	);
}

}  // namespace

bool initializeIMU() {
	imu_initialized = false;
	imu_address = 0;
	read_error_reported = false;

	Wire2.begin();

	if (!device_is_ready(imu_i2c)) {
		Serial.println("MPU6050 initialization failed at I2C3 readiness: controller not ready");
		return false;
	}
	Serial.println("MPU6050 I2C3 controller ready");

	const uint8_t candidate_addresses[] = {
		MPU6050_ADDRESS,
		MPU6050_ALTERNATE_ADDRESS
	};
	const size_t candidate_count =
		sizeof(candidate_addresses) / sizeof(candidate_addresses[0]);
	uint8_t who_am_i_values[2] = {0, 0};
	bool who_am_i_read[2] = {false, false};

	for (size_t i = 0; i < candidate_count; ++i) {
		const int result = readRegisters(
			candidate_addresses[i],
			REG_WHO_AM_I,
			&who_am_i_values[i],
			sizeof(who_am_i_values[i])
		);

		if (result == 0) {
			who_am_i_read[i] = true;
			Serial.print("MPU6050 address 0x");
			Serial.print(
				static_cast<unsigned int>(candidate_addresses[i]),
				HEX
			);
			Serial.print(" responded; WHO_AM_I=0x");
			Serial.println(
				static_cast<unsigned int>(who_am_i_values[i]),
				HEX
			);
			if (who_am_i_values[i] == MPU6050_WHO_AM_I) {
				if (imu_address == 0) {
					imu_address = candidate_addresses[i];
				}
			}
		} else {
			Serial.print("MPU6050 address 0x");
			Serial.print(
				static_cast<unsigned int>(candidate_addresses[i]),
				HEX
			);
			Serial.print(" probe failed; I2C error ");
			Serial.println(result);
		}
	}

	if (imu_address == 0) {
		Serial.println("MPU6050 initialization failed: no address returned WHO_AM_I 0x68");
		for (size_t i = 0; i < candidate_count; ++i) {
			if (who_am_i_read[i]) {
				Serial.print("MPU6050 WHO_AM_I validation failed at address 0x");
				Serial.println(
					static_cast<unsigned int>(candidate_addresses[i]),
					HEX
				);
			}
		}
		return false;
	}

	Serial.print("MPU6050 selected I2C address 0x");
	Serial.println(static_cast<unsigned int>(imu_address), HEX);

	Serial.print("MPU6050 WHO_AM_I=0x");
	Serial.print(static_cast<unsigned int>(MPU6050_WHO_AM_I), HEX);
	Serial.println(" validated");

	// Wake up the MPU6050.
	int result = writeRegister(REG_PWR_MGMT_1, 0x00);
	if (result != 0) {
		reportI2CFailure("power-management register 0x6B write", result);
		return false;
	}
	Serial.println("MPU6050 power-management register 0x6B write succeeded");

	// Accelerometer full-scale range = +/-2g.
	// At this setting the sensitivity is 16384 LSB/g.
	result = writeRegister(REG_ACCEL_CONFIG, 0x00);
	if (result != 0) {
		reportI2CFailure("accelerometer configuration register 0x1C write", result);
		return false;
	}
	Serial.println("MPU6050 accelerometer configuration register 0x1C write succeeded");

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

	const int result = readRegisters(
		imu_address,
		REG_ACCEL_XOUT_H,
		buffer,
		sizeof(buffer)
	);
	if (result != 0) {
		if (!read_error_reported) {
			reportI2CFailure("accelerometer register read", result);
			read_error_reported = true;
		}
		return false;
	}

	if (read_error_reported) {
		Serial.println("MPU6050 accelerometer reads recovered");
		read_error_reported = false;
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

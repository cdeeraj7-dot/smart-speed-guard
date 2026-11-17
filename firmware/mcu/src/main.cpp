#include <Arduino.h>
#include <cmath>
#include <math.h>

#include "telemetry.h"
#include "safety.h"
#include "imu.h"
#include "obstacle_state.h"
#include "Arduino_RouterBridge.h"

TelemetryData telemetry;
SafetyStatus safety_status;
IMUData imu_data;
ObstacleValidityTracker obstacle_validity;

namespace {

constexpr unsigned long TELEMETRY_INTERVAL_MS = 500UL;
unsigned long last_telemetry_ms = 0;
bool telemetry_sent = false;

}  // namespace

void setup() {
    Serial.begin(115200);

    pinMode(LED_BUILTIN, OUTPUT);

    initializeTelemetry(telemetry);
    Bridge.begin();

    safety_status = evaluateSafety(
        telemetry.speed_hall,
        telemetry.obstacle_distance,
        0.0f,
        false,
        telemetry.obstacle_valid
    );

    Serial.println("================================");
    Serial.println("Smart Speed Guard - MCU");
    Serial.println("STM32U585 firmware started");

    bool imu_ok = initializeIMU();

    Serial.println(
        imu_ok ? "MPU6050 initialized" :
                 "MPU6050 initialization FAILED; see preceding I2C diagnostic"
    );

    Serial.println("================================");
}

void loop() {
    const unsigned long now = millis();

    if (telemetry_sent &&
        now - last_telemetry_ms < TELEMETRY_INTERVAL_MS) {
        return;
    }

    telemetry_sent = true;
    last_telemetry_ms = now;
    telemetry.timestamp = now;

    const ObstacleReading obstacle = obstacle_validity.current(now);
    telemetry.obstacle_distance = obstacle.distance_cm;
    telemetry.obstacle_valid = obstacle.valid;

    bool imu_read_ok = readIMU(imu_data);

    bool acceleration_valid =
        imu_read_ok &&
        imu_data.accel_valid &&
        std::isfinite(imu_data.accel_x) &&
        std::isfinite(imu_data.accel_y) &&
        std::isfinite(imu_data.accel_z);

    float acceleration_magnitude = NAN;

    if (acceleration_valid) {
        acceleration_magnitude = sqrtf(
            imu_data.accel_x * imu_data.accel_x +
            imu_data.accel_y * imu_data.accel_y +
            imu_data.accel_z * imu_data.accel_z
        );
        acceleration_valid = std::isfinite(acceleration_magnitude);
    }

    if (!acceleration_valid) {
        acceleration_magnitude = NAN;
    }

    telemetry.sensor_valid = acceleration_valid;

    if (telemetry.sensor_valid) {
        telemetry.accel_x = imu_data.accel_x;
        telemetry.accel_y = imu_data.accel_y;
        telemetry.accel_z = imu_data.accel_z;
    } else {
        telemetry.accel_x = 0.0f;
        telemetry.accel_y = 0.0f;
        telemetry.accel_z = 0.0f;
    }

    telemetry.gyro_x = imu_data.gyro_x;
    telemetry.gyro_y = imu_data.gyro_y;
    telemetry.gyro_z = imu_data.gyro_z;
    telemetry.gyro_valid = imu_data.gyro_valid;

    safety_status = evaluateSafety(
        telemetry.speed_hall,
        telemetry.obstacle_distance,
        acceleration_magnitude,
        telemetry.sensor_valid,
        telemetry.obstacle_valid
    );

    telemetry.deterministic_alert =
        static_cast<uint8_t>(safety_status.alert);

    digitalWrite(
        LED_BUILTIN,
        safety_status.led_active ? LOW : HIGH
    );

    Serial.print("ACCEL X: ");
    Serial.print(telemetry.accel_x, 3);
    Serial.print(" | Y: ");
    Serial.print(telemetry.accel_y, 3);
    Serial.print(" | Z: ");
    Serial.print(telemetry.accel_z, 3);
    Serial.print(" | VALID: ");
    Serial.println(telemetry.sensor_valid ? "YES" : "NO");

    // Full telemetry transmission.
    Bridge.call(
        "telemetry",
        static_cast<unsigned long>(telemetry.timestamp),
        telemetry.speed_hall,
        telemetry.speed_gps,
        telemetry.latitude,
        telemetry.longitude,
        telemetry.gps_valid,
        telemetry.accel_x,
        telemetry.accel_y,
        telemetry.accel_z,
        telemetry.gyro_x,
        telemetry.gyro_y,
        telemetry.gyro_z,
        telemetry.gyro_valid,
        telemetry.obstacle_distance,
        telemetry.deterministic_alert,
        telemetry.sensor_valid
    );
}
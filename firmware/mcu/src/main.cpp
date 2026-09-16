#include <Arduino.h>

#include "telemetry.h"
#include "safety.h"
#include "imu.h"
#include "Arduino_RouterBridge.h"

TelemetryData telemetry;
SafetyStatus safety_status;
IMUData imu_data;

void setup() {
    Serial.begin(115200);

    pinMode(LED_BUILTIN, OUTPUT);

    initializeTelemetry(telemetry);
    Bridge.begin();

    safety_status = evaluateSafety(
        0.0f,
        0.0f,
        0.0f
    );

    bool imu_ok = initializeIMU();

    Serial.println("================================");
    Serial.println("Smart Speed Guard - MCU");
    Serial.println("STM32U585 firmware started");
    Serial.println("Telemetry structure initialized");
    Serial.println("Safety module initialized");

    if (imu_ok) {
        Serial.println("MPU6050 initialized");
    } else {
        Serial.println("MPU6050 initialization FAILED");
    }

    Serial.println("================================");
}

void loop() {

    telemetry.timestamp = millis();

    // Read MPU6050 accelerometer
    bool imu_read_ok = readIMU(imu_data);

    if (imu_read_ok && imu_data.accel_valid) {

        telemetry.accel_x = imu_data.accel_x;
        telemetry.accel_y = imu_data.accel_y;
        telemetry.accel_z = imu_data.accel_z;

        telemetry.sensor_valid = true;

    } else {

        telemetry.accel_x = 0.0f;
        telemetry.accel_y = 0.0f;
        telemetry.accel_z = 0.0f;

        telemetry.sensor_valid = false;
    }

    // Gyroscope intentionally unavailable for now.
    telemetry.gyro_x = 0.0f;
    telemetry.gyro_y = 0.0f;
    telemetry.gyro_z = 0.0f;

    // Current safety evaluation.
    // Speed and obstacle thresholds are not defined yet.
    float acceleration_magnitude = 0.0f;

    safety_status = evaluateSafety(
        telemetry.speed_hall,
        telemetry.obstacle_distance,
        acceleration_magnitude
    );

    // Print real accelerometer telemetry.
    Serial.print("ACCEL X: ");
    Serial.print(telemetry.accel_x, 3);

    Serial.print(" g | Y: ");
    Serial.print(telemetry.accel_y, 3);

    Serial.print(" g | Z: ");
    Serial.print(telemetry.accel_z, 3);

    Serial.print(" g | VALID: ");
    Serial.println(telemetry.sensor_valid ? "YES" : "NO");
    Bridge.call(
    "telemetry",
    telemetry.accel_x,
    telemetry.accel_y,
    telemetry.accel_z,
    telemetry.sensor_valid
);

    delay(500);
}

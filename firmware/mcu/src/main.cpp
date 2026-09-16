#include <Arduino.h>
#include "telemetry.h"
#include "safety.h"

TelemetryData telemetry;
SafetyStatus safety_status;

void setup() {
    Serial.begin(115200);

    pinMode(LED_BUILTIN, OUTPUT);

    initializeTelemetry(telemetry);

    safety_status = evaluateSafety(
        0.0f,
        0.0f,
        0.0f
    );

    Serial.println("================================");
    Serial.println("Smart Speed Guard - MCU");
    Serial.println("STM32U585 firmware started");
    Serial.println("Telemetry structure initialized");
    Serial.println("Safety module initialized");
    Serial.println("================================");
}

void loop() {
    telemetry.timestamp = millis();

    safety_status = evaluateSafety(
        telemetry.speed_hall,
        telemetry.obstacle_distance,
        0.0f
    );

    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("MCU heartbeat: ON");
    delay(1000);

    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("MCU heartbeat: OFF");
    delay(1000);
}
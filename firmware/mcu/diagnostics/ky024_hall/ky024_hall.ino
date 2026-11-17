#include <Arduino.h>

namespace {

constexpr pin_size_t DIGITAL_SENSOR_PIN = D2;
constexpr pin_size_t ANALOG_SENSOR_PIN = A2;

constexpr unsigned long DEBOUNCE_MS = 30UL;
constexpr unsigned long NO_PULSE_TIMEOUT_MS = 5000UL;
constexpr unsigned long PRINT_INTERVAL_MS = 250UL;

PinStatus previousDigitalLevel = LOW;
unsigned long lastAcceptedPulseMs = 0;
unsigned long lastPrintMs = 0;
unsigned long pulseCount = 0;
float lastRpm = 0.0f;
bool haveAcceptedPulse = false;
bool haveRpm = false;

}  // namespace

void setup() {
	Serial.begin(115200);

	pinMode(DIGITAL_SENSOR_PIN, INPUT);
	analogReadResolution(10);

	// Use the startup level as the baseline; do not count a startup state.
	previousDigitalLevel = digitalRead(DIGITAL_SENSOR_PIN);
	lastPrintMs = millis();

	Serial.println("KY-024 Hall sensor diagnostic");
	Serial.println("Counting D2 (module D0) LOW-to-HIGH transitions only.");
	Serial.println("RPM assumes one magnet per revolution.");
}

void loop() {
	const unsigned long now = millis();
	const PinStatus digitalLevel = digitalRead(DIGITAL_SENSOR_PIN);

	// A single rising edge represents one passage; debounce rejects rapid repeats.
	if (previousDigitalLevel == LOW && digitalLevel == HIGH) {
		if (!haveAcceptedPulse ||
			now - lastAcceptedPulseMs >= DEBOUNCE_MS) {
			if (haveAcceptedPulse) {
				const unsigned long pulseIntervalMs =
					now - lastAcceptedPulseMs;
				lastRpm = 60000.0f / pulseIntervalMs;
				haveRpm = true;
			}

			++pulseCount;
			lastAcceptedPulseMs = now;
			haveAcceptedPulse = true;
		}
	}

	previousDigitalLevel = digitalLevel;

	if (now - lastPrintMs >= PRINT_INTERVAL_MS) {
		lastPrintMs = now;
		const int analogLevel = analogRead(ANALOG_SENSOR_PIN);

		Serial.print("D2/D0=");
		Serial.print(digitalLevel == HIGH ? "HIGH" : "LOW");
		Serial.print(" | A2/A0=");
		if (analogLevel < 0) {
			Serial.print("ADC error ");
			Serial.print(analogLevel);
		} else {
			Serial.print(analogLevel);
		}
		Serial.print(" | Pulses=");
		Serial.print(pulseCount);
		Serial.print(" | RPM=");

		if (!haveAcceptedPulse ||
			now - lastAcceptedPulseMs >= NO_PULSE_TIMEOUT_MS) {
			Serial.println("0.00 | No pulses detected recently");
		} else if (!haveRpm) {
			Serial.println("waiting for a second pulse");
		} else {
			Serial.println(lastRpm, 2);
		}
	}
}

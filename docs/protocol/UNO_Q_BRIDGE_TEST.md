# UNO Q Bridge Test Reference

This is the known-good UNO Q Linux-to-STM32 Bridge test and the current
MCU-to-Linux telemetry contract observed in this repository.

## MCU/Linux telemetry contract (current verified schema)

The current repository MCU sketch sends one 16-field Bridge callback payload in
this exact order:

1. `mcu_timestamp_ms`
2. `speed_hall`
3. `speed_gps`
4. `latitude`
5. `longitude`
6. `gps_valid`
7. `accel_x`
8. `accel_y`
9. `accel_z`
10. `gyro_x`
11. `gyro_y`
12. `gyro_z`
13. `gyro_valid`
14. `obstacle_distance`
15. `deterministic_alert`
16. `sensor_valid`

The repository Linux receiver writes those values to `telemetry.csv` with the
same column order. This contract is defined in `firmware/linux/bridge_contract.py`
and is enforced by the Linux-side validation helper before the row is appended.

The contract is a schema definition for the current implementation; it does not
establish that each physical sensor is valid, calibrated, or available.
Hall-speed, GPS, obstacle distance, and gyroscope acquisition remain
unimplemented or unverified in the present MCU source.

## STM32U585 sketch

```cpp
#include "Arduino_RouterBridge.h"

void set_led_state(bool state) {
	digitalWrite(LED_BUILTIN, state ? LOW : HIGH);
}

void setup() {
	pinMode(LED_BUILTIN, OUTPUT);

	Bridge.begin();
	Bridge.provide_safe("set_led_state", set_led_state);
}

void loop() {
}
```

## Linux-side Python script

```python
from arduino.app_utils import App, Bridge
import time

led_state = False

def loop():
	global led_state

	time.sleep(1)
	led_state = not led_state

	Bridge.call("set_led_state", led_state)

	print("Bridge command:", "LED ON" if led_state else "LED OFF")

App.run(user_loop=loop)
```

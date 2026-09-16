# UNO Q Bridge Test Reference

This is the known-good UNO Q Linux-to-STM32 Bridge test.

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

## Current Status

The current implementation is a verified bring-up test.

It receives real accelerometer X, Y, and Z values from the STM32U585 MCU
through the Arduino Bridge and processes them in the QRB2210 Linux
environment.

The receiver also logs the received telemetry to a CSV file on the UNO Q
Linux filesystem.

Current verified flow:

MPU6050
↓
STM32U585
↓
Arduino Bridge
↓
QRB2210 Linux
↓
Python telemetry receiver
↓
CSV logging

The current telemetry message is intentionally limited to accelerometer data.
It will be extended to the project's structured telemetry format as additional
sensors are integrated.
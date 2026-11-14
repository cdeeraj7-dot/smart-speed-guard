## Current Status

The initial accelerometer-only Bridge bring-up was verified. The current MCU
sketch sends an expanded telemetry message through the Arduino Bridge, and the
Linux receiver is configured to log its fields to a CSV file on the UNO Q
Linux filesystem.

Current intended flow:

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

Only the accelerometer values are currently acquired by the MCU implementation.
Hall speed, GPS, obstacle distance, and gyro values are transmitted as present
in the telemetry structure; their sensor acquisition is not yet implemented.
End-to-end operation of the expanded message is NOT YET MEASURED.
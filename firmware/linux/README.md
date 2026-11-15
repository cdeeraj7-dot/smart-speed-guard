## Current Status

The initial accelerometer-only Bridge bring-up was verified. The current MCU
sketch sends an expanded telemetry message through the Arduino Bridge, and the
repository's Linux receiver source is configured to log its fields to a CSV
file on the UNO Q Linux filesystem.

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
Two safe-bench observations verified delivery of the expanded message to the
current receiver and CSV logging, including a recheck after restarting the
receiver. Sensor accuracy, unimplemented sensor fields, recovery behavior, and
Linux/Bridge failure independence remain unverified.

## App Lab deployment status — 2026-11-15

The user manually pasted `firmware/linux/receiver.py` into Arduino App Lab
0.12.0, `Telemetry Receiver Test` → `python/main.py`. With the repository MCU
firmware uploaded over USB `COM5`, the app logged repeated `Telemetry logged`
callbacks. The `telemetry.csv` file appeared in the App Lab file tree; its
viewed snapshot contained the expected 16-column header and 35 data rows, each
with 16 fields. This verifies callback ordering and CSV logging in one
safe-bench run, not sensor accuracy or system-level failure handling.

App Lab's Stop action also stopped the microcontroller, so it is not a
Linux-only fault injector. With the Python receiver stopped, a host serial
sample showed 11 local `ACCEL` lines in 5.07 s at approximately 500 ms
intervals. This does not show that the Linux Bridge service itself was
unavailable, or measure a failure-case `Bridge.call()` duration.

After App Lab Run restarted the receiver, the repository firmware was
re-uploaded over USB `COM5`. The first flash attempt timed out in OpenOCD; the
single retry completed successfully. The receiver remained running, and fresh
callback logs continued with increasing MCU timestamps, reaching 250,097 ms
in the latest inspected log window. After reopening `telemetry.csv`, the
visible snapshot contained 31 data rows; the header and every visible row had
16 fields, with timestamps from 232,093 to 247,096 ms. This is not a confirmed
total-file row count. The App Lab Run action flashes its own sketch, so
re-upload the repository firmware after each Run to restore the current MCU
sender. At the last observation, both the receiver and repository firmware
were running. The separate `Smart Speed Guard MCU` project's Python entry
point is still a `Hello world!` stub, and its `imu.cpp` uses `Wire2` rather
than the repository's user-confirmed `Wire` edit.
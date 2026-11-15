# MCU Firmware Build

## Target

- Board: Arduino UNO Q
- Arduino CLI FQBN: `arduino:zephyr:unoq`
- Verified local core: `arduino:zephyr` 1.0.0
- Verified local Bridge library: `Arduino_RouterBridge` 0.4.3

Arduino's sketch format requires a root `.ino` file named after its sketch
folder. `mcu.ino` is the sketch entry file; MCU implementation files are in
`src/`, which Arduino CLI compiles recursively. The headers are in `include/`,
so the build command adds that folder to the C++ include path.

## Compile from the repository root

With Arduino CLI available on `PATH`, run:

```powershell
arduino-cli compile --fqbn arduino:zephyr:unoq --build-property "compiler.cpp.extra_flags=-Ifirmware/mcu/include" firmware\mcu
```

In the verified Windows IDE installation, the CLI is bundled here if it is not
on `PATH`:

```powershell
$cli = "$env:LOCALAPPDATA\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
& $cli compile --fqbn arduino:zephyr:unoq --build-property "compiler.cpp.extra_flags=-Ifirmware/mcu/include" firmware\mcu
```

The command above compiled successfully on 2026-11-14 using Arduino CLI 1.5.1,
the UNO Q `arduino:zephyr` 1.0.0 core, and `Arduino_RouterBridge` 0.4.3.
Compilation does not verify flashing, sensor wiring, sensor readings, or
physical MCU/Linux Bridge communication.

## Safety-state prototype and timing status

The current MCU safety logic in `src/safety.cpp` implements a conservative,
non-blocking alert-state machine with provisional hysteresis thresholds. These
values are development defaults only and must be replaced by measured,
bench-validated parameters before any field deployment or safety claim.

Watchdog configuration is **PENDING TIMING MEASUREMENTS**. No watchdog is
enabled, and no timeout or feed condition is selected. Do not configure one
until actual measurements are available and the proposed timeout/feed policy
has been approved.

Reset-to-setup-entry time, failure-case timing, and guaranteed worst-case
execution bounds are **NOT YET MEASURED**.

### Safe-bench measurement — 2026-11-15

A temporary timing-profile build was run on the Arduino UNO Q 2GB using
`micros()`. The profile was compiled and uploaded for measurement, then removed;
the normal repository firmware was rebuilt, uploaded, and its startup output
confirmed. No watchdog code or settings were added.

| Operation | Measured result |
|---|---|
| `setup()` from function entry through the startup banner | 123,874 us (one run); excludes reset-to-setup-entry |
| `Bridge.begin()` | 3 us (one run) |
| `initializeIMU()` | 100,240 us (one run; includes the existing 100 ms delay) |
| `readIMU()` | 260 us observed maximum across 780 profiled cycles |
| Existing telemetry serial output | 2,217 us observed maximum across 780 profiled cycles |
| `Bridge.call()` | 84,350 us observed maximum across 780 profiled cycles |
| Full measured telemetry cycle through `Bridge.call()` return | 86,629 us observed maximum across 780 profiled cycles |

These are observed values, not guaranteed execution bounds. The measured cycle
included timing-instrumentation overhead, which was not separately measured.
The sensor reported valid accelerometer samples during the capture; this does
not establish calibration, accuracy, or failure behavior.

The current-schema Linux receiver was not verified as active during this
timing run, so these timings alone do not establish end-to-end delivery or
Linux-failure independence. A separate receiver check is recorded below.

The timing profile was temporary and is not present in the repository source.
The normal source firmware was recompiled and uploaded after the run. The
observed maxima below are based on completed 60-cycle profile windows; later
partial samples were not included in their aggregate.

### Receiver callback and receiver-app-stopped observation — 2026-11-15

The user pasted `firmware/linux/receiver.py` into Arduino App Lab 0.12.0,
`Telemetry Receiver Test` → `python/main.py`. With the repository MCU firmware
uploaded over USB `COM5`, the app log showed repeated `Telemetry logged`
callbacks carrying the current 16-field payload. The `telemetry.csv` file
appeared in the App Lab file tree; its viewed snapshot contained the expected
16-column header and 35 data records, each with 16 fields.

To check local MCU progress without the Python receiver, the App Lab Stop
action was used. Its log also said `Stopping microcontroller...`, so this
action is not a Linux-only failure injector and halted the MCU as well. The
normal repository firmware was uploaded again over `COM5` while the Python app
remained stopped. A host serial read at 115200 baud, after discarding buffered
input, received 11 `ACCEL` lines in 5.07 s at approximately 500 ms intervals.
This confirms repeated local sensor/serial cycles while the Python receiver
app was absent. It does not establish that the Linux Bridge service itself was
unavailable, measure `Bridge.call()` duration in that condition, or establish
a worst-case bound.

The initial callback/CSV snapshot is a safe-bench verification, not validation
of sensor accuracy or fields whose acquisition is not implemented.
Reset-to-setup-entry timing and controlled I²C failure behavior remain
**NOT YET MEASURED**. Watchdog configuration remains deferred.

### Receiver restart and post-upload callback check — 2026-11-15

After App Lab Run restarted the receiver and flashed its own sketch, the
repository firmware was recompiled and uploaded over USB `COM5`. The first
flash attempt timed out in OpenOCD; the retry completed successfully with
exit code 0. The running receiver then logged fresh callbacks with increasing
MCU timestamps. The latest inspected log window contained 45 distinct callback
timestamps from 228,092 to 250,097 ms.

After reopening `telemetry.csv`, the visible editor snapshot contained 31
data rows; the header and every visible row had 16 fields, with timestamps
from 232,093 to 247,096 ms. This is a view snapshot, not a confirmed total
file row count. The receiver and repository firmware were running at the last
observation. These checks do not establish sensor accuracy or Linux/Bridge
failure independence.

Known operations that require measurement on the target:

| Operation | Current code path | Known behavior | Measured result / remaining status |
|---|---|---|---|
| MPU6050 initialization | `initializeIMU()` in `src/imu.cpp` | Calls `Wire.begin()`, writes registers, then has a fixed `delay(100)`. | 100,240 us observed once; failure case NOT YET MEASURED |
| MPU6050 acquisition | `readIMU()` and `readRegisters()` in `src/imu.cpp` | Performs synchronous I²C register selection and read. Timeout/bus failure duration is not characterized. | 260 us observed maximum over 780 cycles; I²C failure NOT YET MEASURED |
| Serial diagnostics | `loop()` in `src/main.cpp` | Prints accelerometer values each telemetry cycle. | 2,217 us observed maximum over 780 cycles |
| Bridge transmission | `Bridge.call()` in `src/main.cpp` | Sends the telemetry payload synchronously from the loop. Callback delivery was confirmed in two safe-bench app runs; the receiver-app-stopped serial sample showed later MCU cycles, but did not isolate Linux/Bridge service failure or time the call. | 84,350 us observed maximum over 780 normal-profile cycles; failure-case duration and guaranteed bound NOT YET MEASURED |
| Full telemetry cycle | `loop()` in `src/main.cpp` | Starts a cycle every 500 ms or later; interval is not a measurement of execution duration. | 86,629 us observed maximum over 780 cycles |
| Reset to setup completion | MCU reset through `setup()` | Requires an external or reset-triggered timing reference. | NOT YET MEASURED |

### Measurement plan

For remaining measurements, use the UNO Q with a controlled sensor/Bridge setup
and a receiver confirmed to match the current 16-field payload:

1. Capture reset-to-setup-complete time, and separately time `Bridge.begin()`
   and `initializeIMU()`. Include the existing 100 ms IMU delay in the measured
   initialization duration.
2. Measure repeated `readIMU()`, serial diagnostics, and `Bridge.call()` durations
   separately, as well as total cycle execution from cycle start through
   `Bridge.call()` return.
3. Collect enough cycles to observe maximum durations under normal sensor
   reads, I²C error/timeout conditions, active Linux telemetry reception,
   receiver-app unavailable, and Linux/Bridge service unavailable as separate
   conditions. Report sample count, setup, observed maxima, and instrumentation
   overhead. Do not label an observed maximum a guaranteed bound.
4. Record the actual time source and measurement method. Prefer externally
   observed timing or buffered measurements so diagnostic printing does not
   dominate the measured interval; verify any diagnostic build separately.
5. Confirm that Linux/Bridge service failure cannot starve the next MCU safety
   cycle. The receiver-app-stopped check above is not a full Linux/Bridge
   service failure test. If `Bridge.call()` can block without a verified
   bound, the independent safety-path requirement is not demonstrated.
6. Only after these measurements, propose a watchdog timeout with a documented
   safety margin and feed it only after essential safety tasks complete
   successfully. Obtain approval before implementing or enabling it.

Arduino's official references:

- [UNO Q hardware and development workflow](https://docs.arduino.cc/hardware/uno-q/)
- [Arduino CLI sketch specification](https://arduino.github.io/arduino-cli/1.6/sketch-specification/)

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

## Timing and watchdog status

Watchdog configuration is **PENDING TIMING MEASUREMENTS**. No watchdog is
enabled, and no timeout or feed condition is selected. Do not configure one
until actual measurements are available and the proposed timeout/feed policy
has been approved.

Actual MCU startup time, initialization time, steady-state loop execution time,
and worst-case loop duration under sensor and communication workloads are all
**NOT YET MEASURED**. The build host detected no connected Arduino board on
2026-11-14, so no timing measurements or firmware flashing were performed.

Known operations that require measurement on the target:

| Operation | Current code path | Known behavior | Maximum execution time |
|---|---|---|---|
| MPU6050 initialization | `initializeIMU()` in `src/imu.cpp` | Calls `Wire.begin()`, writes registers, then has a fixed `delay(100)`. The delay alone is 100 ms; total initialization duration is unknown. | NOT YET MEASURED |
| MPU6050 acquisition | `readIMU()` and `readRegisters()` in `src/imu.cpp` | Performs synchronous I²C register selection and read. Timeout/bus failure duration is not characterized. | NOT YET MEASURED |
| Serial diagnostics | `loop()` in `src/main.cpp` | Prints accelerometer values each telemetry cycle. Output duration depends on runtime/transport. | NOT YET MEASURED |
| Bridge transmission | `Bridge.call()` in `src/main.cpp` | Sends the telemetry payload synchronously from the loop. Blocking behavior, especially when Linux is unavailable, has not been characterized. | NOT YET MEASURED |
| Full telemetry cycle | `loop()` in `src/main.cpp` | Starts a cycle every 500 ms or later; interval is not a measurement of execution duration. | NOT YET MEASURED |

### Measurement plan

With the UNO Q connected and a controlled sensor/Bridge setup:

1. Capture reset-to-setup-complete time, and separately time `Bridge.begin()`
   and `initializeIMU()`. Include the existing 100 ms IMU delay in the measured
   initialization duration.
2. Measure repeated `readIMU()`, serial diagnostics, and `Bridge.call()` durations
   separately, as well as total cycle execution from cycle start through
   `Bridge.call()` return.
3. Collect enough cycles to observe maximum durations under normal sensor
   reads, I²C error/timeout conditions, active Linux telemetry reception, and
   Linux unavailable. Report sample count, setup, observed maxima, and
   instrumentation overhead. Do not label an observed maximum a guaranteed
   bound.
4. Record the actual time source and measurement method. Prefer externally
   observed timing or buffered measurements so diagnostic printing does not
   dominate the measured interval; verify any diagnostic build separately.
5. Confirm that Linux/Bridge failure cannot starve the next MCU safety cycle.
   If `Bridge.call()` can block without a verified bound, the independent
   safety-path requirement is not yet demonstrated.
6. Only after these measurements, propose a watchdog timeout with a documented
   safety margin and feed it only after essential safety tasks complete
   successfully. Obtain approval before implementing or enabling it.

Arduino's official references:

- [UNO Q hardware and development workflow](https://docs.arduino.cc/hardware/uno-q/)
- [Arduino CLI sketch specification](https://arduino.github.io/arduino-cli/1.6/sketch-specification/)

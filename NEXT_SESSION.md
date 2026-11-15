# Smart Speed Guard — Next Session

## Exact stopping point

Stage 0 audit reconciliation and Stage 1 repository/build setup are complete.
Stage 2 MCU foundation remains in progress. Safe-bench timing, callback/CSV
logging, and a receiver-app-stopped local serial observation were verified.
The normal repository MCU firmware and App Lab Python receiver are currently
running. See [firmware/mcu/README.md](./firmware/mcu/README.md) for measured
observations and limitations. Watchdog configuration is **PENDING TIMING
MEASUREMENTS** and user approval; no timeout or feed policy has been selected.

## Current state and next steps

Stage 2 remains PARTIAL / IN PROGRESS. The remaining Stage 2 work is limited to
MCU foundation evidence: startup timing, loop cadence, serial/Bridge blocking,
independent local operation without Linux, and measured recovery after service or
bus failure. Stage 3 sensor electrical validation, Stage 4 calibration/
filtering acceptance, and Stage 5 safety-threshold tuning remain separate later
requirements.

The user pasted `firmware/linux/receiver.py` into Arduino App Lab 0.12.0 →
`Telemetry Receiver Test` → Files → `python` → `main.py`. The receiver logged
repeated 16-field callbacks. The original `telemetry.csv` snapshot had the
expected 16-column header and 35 data rows, each with 16 fields.

The App Lab Stop action stopped both the Python container and the MCU. After
re-uploading the repository firmware through USB `COM5`, the Python receiver
remained stopped. A host serial capture after discarding buffered input saw 11
local `ACCEL` lines in 5.07 s at approximately 500 ms intervals. This is a
receiver-app-stopped observation, not a Linux/Bridge-service outage test or a
direct measurement of `Bridge.call()` duration.

After App Lab Run restarted the receiver, the repository firmware was
re-uploaded to `COM5`. The first flash attempt timed out in OpenOCD; the
retry completed successfully. The receiver remained running and fresh
callbacks resumed. The latest inspected log window showed 45 distinct MCU
timestamps from 228,092 to 250,097 ms. Reopening `telemetry.csv` showed 31
visible data rows with 16 fields each, spanning 232,093–247,096 ms; this is
not a full-file row count.

Current board/app state: repository MCU firmware and the App Lab receiver are
running. App Lab Run flashes its own sketch, so re-upload the repository
firmware after each Run to restore the current MCU sender. App Lab Stop also
stops the MCU.

## Last completed task

- Verified repeated 16-field Bridge callbacks and CSV logging after the user
  pasted the repository receiver into App Lab.
- Re-uploaded normal repository MCU firmware over USB `COM5`.
- Restarted the App Lab receiver, restored repository firmware after App Lab
  Run, and re-verified callback logging and a visible 16-field CSV snapshot.
- Observed 11 local serial telemetry lines over 5.07 s with the Python
  receiver app stopped; App Lab Stop also halts the MCU, so firmware had to be
  uploaded again before this observation.
- See `DEVELOPMENT_LOG.md` and `firmware/mcu/README.md` for exact results,
  caveats, and earlier timing measurements.

## Remaining Stage 2 validation requirements

The following requirements are Stage 2 blockers and must be measured before
Stage 2 acceptance is reconsidered. Stage 3 sensor electrical validation,
Stage 4 filter/calibration acceptance, and Stage 5 safety-threshold approval are
separate and are not Stage 2 completion criteria.

1. Measure reset-to-setup timing and direct `Bridge.call()` durations under
   active receiver, receiver-app-stopped, and Linux/Bridge service failure.
   Keep those conditions separate. Existing measured values are summarized in
   `firmware/mcu/README.md`; the remaining item is the missing failure/recovery
   evidence.
2. Measure I²C failure behavior using a controlled, electrically safe setup.
   The failure case remains NOT YET MEASURED.
3. Measure serial communication failure behavior without using App Lab Stop as a
   Linux-only failure injector, because App Lab Stop also stops the MCU.
4. Verify that local MCU safety operation continues while the Linux/Bridge path
   is unavailable, and record recovery when the service or bus becomes available
   again.
5. Keep the current 16-field Bridge/receiver/CSV schema, MCU timestamp, and
   validity fields. Do not populate unintegrated sensors with invented
   readings.
6. Record future validation as measured only when logs/results exist; the
   watchdog stays deferred pending measurements and user approval.

### Exact additional measurements still required

Measured already:
- `setup()` entry-to-banner timing: 123,874 us (single observation)
- `Bridge.begin()` timing: 3 us
- `initializeIMU()` timing: 100,240 us
- `readIMU()` observed maximum: 260 us across 780 cycles
- serial output observed maximum: 2,217 us across 780 cycles
- `Bridge.call()` observed maximum: 84,350 us across 780 cycles
- full measured step through `Bridge.call()` return: 86,629 us across 780 cycles

Still required for Stage 2 evidence:
- reset-to-setup completion timing, including exact reset-source definition and
  time source
- direct `Bridge.call()` duration while the Linux receiver is active and while
  the Linux/Bridge service is unavailable, reported separately
- serial output failure duration while the host monitor/serial path is stalled
  or disconnected
- I²C failure detection time and recovery behavior for the MPU6050 bus
- proof that the MCU loop continues local safety progression with no Linux or
  Bridge callback delivery
- proof that the system recovers cleanly after the downstream service or bus is
  restored

### Safe-bench validation procedure (do not execute without explicit user approval)

#### A. Reset-to-setup timing

Required hardware/software:
- UNO Q board, USB cable, host PC
- Arduino CLI or IDE upload workflow already used in the repo
- serial monitor or host logger on the COM port
- known-good repository firmware (do not use App Lab Run as the reset source)

Manual actions:
- Power-cycle the board or issue a hardware reset while the host logs the COM
  port timestamps.
- Start timer at the moment the reset line is asserted or the board loses power;
  stop at the first MCU startup banner or consistent serial output sequence.
- Repeat 5-10 times if a stable sample is needed.

Expected observations:
- Board restarts, prints the startup banner, and resumes sensor and telemetry
  activity.
- No MCU deadlock or unresponsive reset path.

How to record results:
- log each reset number, wall-clock time, reset trigger, observed output line,
  and measured interval in milliseconds.

Pass/fail:
- Pass: reset-to-startup timing is measured and recorded consistently; no
  blocked startup or repeated reset loops.
- Fail: board does not reach the startup banner, stalls, or resets repeatedly.

Restore working state:
- reflash the repository firmware and confirm the normal telemetry loop resumes.

#### B. Controlled Linux/Bridge service failure

Required hardware/software:
- UNO Q board with repository MCU firmware
- host PC running the current Python receiver or equivalent Bridge service
- method to terminate the receiver process without resetting the MCU
- serial monitor or host logger

Manual actions:
- Start the receiver as normal.
- Confirm telemetry callback logs are active.
- Stop the Linux receiver by terminating the process on the host, not by using
  App Lab Stop, because App Lab Stop also stops the MCU.
- Leave the MCU powered and running, while capturing serial output from the COM
  port.
- Restart the receiver after a fixed delay and confirm logging resumes.

Expected observations:
- The MCU continues to run its local loop and serial output even when the
  Linux/Bridge callback path is unavailable.
- The local safety path should keep running; no MCU-wide stall should occur.
- After the receiver restarts, callback/CSV logging resumes without a manual MCU
  reset.

How to record results:
- log the exact time the Linux receiver was stopped, the serial activity during
  the outage, the exact time resumed, and callback counts.

Pass/fail:
- Pass: MCU continues to run locally, serial output continues, and recovery is
  clean once the service returns.
- Fail: MCU stalls, watchdog would be required, or the local loop stops while
  Linux is unavailable.

Restore working state:
- restart the receiver and restore the normal repository firmware if needed.

#### C. Serial communication failure

Required hardware/software:
- UNO Q board with repository firmware
- host USB serial terminal or logger
- method to interrupt or pause serial host read without resetting the board

Manual actions:
- Run the MCU normally and then pause, disconnect, or stop the host serial port
  from draining output while the MCU continues to run.
- Keep the board powered and leave the serial Tx line active.
- Resume monitoring after a measured interval.

Expected observations:
- Serial logging may stall or drop; the MCU loop should continue local telemetry
  and local safety updates without dependency on Host terminal drainage.

How to record results:
- time stamps of when the port was paused/closed and when resumed; note any
  missed or delayed serial lines.

Pass/fail:
- Pass: local MCU operation continues and no reset or deadlock occurs.
- Fail: the MCU blocks on serial output or otherwise stalls.

Restore working state:
- reconnect the terminal and confirm normal serial output resumes.

#### D. I2C/MPU6050 communication failure

Required hardware/software:
- UNO Q board with IMU connected on the verified I²C bus
- host serial logger
- safe-bench electrical access to isolate or disconnect the sensor without
  creating an unsafe condition

Manual actions:
- Put the board in a known-good state and confirm sensor read success.
- Isolate the bus, remove the sensor from the test bench only in a safe,
  controlled manner, or use an equivalent controlled bus-failure setup
  approved for the bench.
- Observe whether `readIMU()` fails promptly and whether the MCU continues to
  run. If the bus is deliberately disconnected, restore it after the test.

Expected observations:
- `initializeIMU()` or `readIMU()` should fail cleanly and return false or an
  invalid status if the bus is unavailable.
- The loop should continue to execute and not deadlock indefinitely.

How to record results:
- log timestamps around the failure, the observed `VALID`/`INVALID` state, and
  the duration until the MCU resumes operation.

Pass/fail:
- Pass: failure is detected quickly, logged as invalid, and does not stall the
  local loop.
- Fail: hang, repeated lockup, or failure that blocks local safety operation.

Restore working state:
- reconnect the IMU and verify `MPU6050 initialized` and valid sample output.

#### E. MCU local operation during Linux/Bridge unavailability

Required hardware/software:
- UNO Q board with repository firmware
- host serial monitor
- a receiver process or service that can be stopped without resetting the MCU
- optional host-side process supervisor for recording receiver uptime

Manual actions:
- Start the MCU with Linux receiver disabled or stopped.
- Capture local serial lines and timestamp intervals.
- Observe whether the MCU continues to emit telemetry or safety-state output even
  when the Bridge callback path is not available.

Expected observations:
- Local serial loop continues on the MCU without dependency on Linux or Bridge.

How to record results:
- serial log, sample counts, timestamp intervals, and whether Bridge callback
  attempts are absent while the board continues to run.

Pass/fail:
- Pass: local operation continues and safety logic remains active.
- Fail: no local loop activity or stall while Bridge path is absent.

Restore working state:
- restart the Linux receiver or Bridge service and confirm callback delivery.

#### F. Recovery after the failed service or interface becomes available again

Required hardware/software:
- same as the specific failure being tested
- host logs for both serial and receiver/CSV output

Manual actions:
- trigger the failure, wait for a fixed observation period, then restore the
  service or bus.
- observe whether callback logs and serial logs resume without a manual reset.

Expected observations:
- Clean recovery with resumed telemetry and no permanent stuck state.

How to record results:
- timestamps for failure start, service restore, and first successful callback or
  valid sensor sample after recovery.

Pass/fail:
- Pass: recovered state is stable and normal telemetry resumes.
- Fail: partial recovery, permanent outage, or repeated stall.

Restore working state:
- restore the board to its normal observation state and verify telemetry logs are
  complete and readable.

### Manual-vs-software split

Tests that must be performed manually on real hardware:
- Reset-to-setup timing
- Linux/Bridge service failure
- Serial communication failure
- I²C/MPU6050 communication failure
- Local MCU operation during Bridge outage
- Recovery once service or bus returns

Tests that can be performed through software without hardware:
- Repository build and compile checks
- Python unit tests covering the Bridge schema and contract validation
- Source-level checks for invalid payloads and CSV schema consistency
- developer review of startup logic, local safety logic, and logging contract
  against the verified repo state

The hardware tests above remain the only accepted evidence for Stage 2
completion; software checks alone do not satisfy the hardware validation gate.

## Relevant files and symbols

- `firmware/mcu/src/main.cpp` — `setup()` and `loop()`; MCU telemetry assembly
  and Bridge payload.
- `firmware/mcu/include/telemetry.h` — `TelemetryData`, including validity
  fields.
- `firmware/mcu/src/telemetry.cpp` — `initializeTelemetry()`.
- `firmware/mcu/src/imu.cpp` and `firmware/mcu/include/imu.h` — current IMU
  acquisition and validity behavior.
- `firmware/linux/receiver.py` — Bridge callback and CSV schema.
- `docs/protocol/UNO_Q_BRIDGE_TEST.md` — existing Bridge bring-up reference;
  verify its applicability to the current expanded payload.
- `docs/architecture/ARCHITECTURE_AUDIT.md` — reconciled source inventory;
  board/toolchain/electrical/protocol decisions remain unresolved.
- `PROJECT_PROGRESS.md`, `DEVELOPMENT_LOG.md`, `NEXT_SESSION.md`,
  `PHASE_CHECKLIST.md`, `CHANGELOG.md` — persistent checkpoint documents.

## Known issues and limits

- Stage 0 audit and Stage 1 build setup are complete; technical/hardware
  verification questions remain open.
- The UNO Q 2GB, `arduino:zephyr:unoq` target, installed CLI/core, and intended
  `Wire` bus are confirmed for this workspace. Pin/electrical details,
  watchdog behavior, and inter-domain runtime behavior remain unverified.
- The CLI build passes; IDE GUI compilation remains unverified. On 2026-11-15,
  the repository MCU firmware was uploaded over `COM5`, and startup output,
  callback delivery, and visible CSV rows were observed on the connected
  board.
- Callback delivery was observed in two App Lab runs, with a CSV snapshot
  checked in each. IMU samples were marked valid during the observed runs.
  Sensor calibration, accuracy, controlled I²C failure, Linux/Bridge service
  failure, and broader physical behavior remain unverified.
- Watchdog configuration is **PENDING TIMING MEASUREMENTS**. Do not select or
  hardcode a timeout, enable the hardware watchdog, or introduce automatic
  watchdog resets. Feed policy requires essential-task success and user approval.
- Known blocking paths needing target measurements: `initializeIMU()` includes
  `delay(100)` and synchronous `Wire` calls; `readIMU()` uses synchronous I2C;
  `Serial.print` and `Bridge.call()` may block. Normal-case sample maxima are
  listed in `firmware/mcu/README.md`; failure maxima and guaranteed bounds are
  NOT YET MEASURED.
- Hall speed, GPS, obstacle distance, and gyro acquisition are not established
  by the current telemetry sender; do not treat transmitted defaults as
  measurements.
- Current worktree changes are uncommitted. No change should be reverted,
  committed, or pushed without explicit user direction.
- The user confirmed the pending `Wire2`-to-`Wire` change in
  `firmware/mcu/src/imu.cpp` matches the actual wiring; physical sensor reads
  were observed as valid on 2026-11-15, but calibration and failure behavior
  remain unverified.
- App Lab `Telemetry Receiver Test` contains the user-pasted current receiver
  source and is running at the last observation. Its Stop action also stops
  the MCU; App Lab Run flashes its own sketch, so restore repository firmware
  afterward. The separate `Smart Speed Guard MCU` project still has a
  `Hello world!` Python entry point and stale `Wire2` IMU code.

## Monday integration preparation

Before any wiring or hardware test:

- Confirm the exact board and peripheral/module versions available.
- Verify official pin, voltage, and interface requirements; leave unresolved
  mappings as `TODO: VERIFY PIN MAPPING`.
- Confirm the MCU build target and toolchain.
- Define a test sequence for compile/flash, IMU validity and failure behavior,
  Bridge field ordering, and Linux CSV logging.
- Record physical-test results separately from software tests; do not claim a
  test passed until it has actually run.

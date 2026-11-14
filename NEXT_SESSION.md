# Smart Speed Guard — Next Session

## Exact stopping point

Stage 0 audit reconciliation and Stage 1 repository/build setup are complete.
Stage 2 MCU foundation is in progress; the elapsed-time scheduling increment
compiles for UNO Q. Arduino CLI detected no attached board, so timing data,
flashing, sensor behavior, and Bridge failure behavior remain unverified.
Watchdog configuration is **PENDING TIMING MEASUREMENTS**; no timeout or feed
policy has been selected. See
[PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md) for all uncommitted files.

## Current task

When the board is connected, measure reset-to-ready/startup time, Bridge and IMU
initialization, `readIMU()`, serial output, `Bridge.call()`, and total
steady-state/worst-case cycle duration under normal and failure conditions.
Confirm Linux/Bridge failure does not starve MCU safety work. Then propose a
watchdog timeout/feed policy with measured safety margin for user approval.
Do not enable/configure a watchdog before approval.

## Last completed task

- Inspected the current source, architecture audit, Git history, and working
  tree.
- Added the progress, development log, next-session, phase checklist, and
  changelog files.
- Ran the full Python test suite (111 passed) and Python compileall (passed).
- Began Stage 0 reconciliation after reviewing the pre-existing source diffs.
- Reconciled the architecture audit inventory and completed Stage 0.
- Completed Stage 1 by adding the sketch entry/build guide and compiling the
  MCU for `arduino:zephyr:unoq`.
- Began Stage 2 with a checkpoint to replace `delay(500)` while preserving the
  payload and first-send behavior.
- Replaced the delay with elapsed-time gating and verified the UNO Q compile.
- Recorded that watchdog configuration is PENDING TIMING MEASUREMENTS; board
  detection found no attached board, so actual timing data could not be taken.
- Reran Python tests (111 passed), compileall (passed), UNO Q compile (passed),
  and whitespace check (passed).

## Remaining subtasks

1. Attach the UNO Q and follow the timing procedure in `firmware/mcu/README.md`.
   Actual startup/init/loop timing and blocking-operation maxima are NOT YET
   MEASURED.
2. Verify sensor wiring and electrical interfaces from official documentation
   and available hardware. Until verified, keep unknown mappings marked
   `TODO: VERIFY PIN MAPPING`.
3. Review the current 16-field Bridge/receiver/CSV schema and retain the MCU
   timestamp and validity fields. Do not populate unintegrated sensors with
   invented readings.
4. With hardware available, test the MCU sensor read path and Bridge callback;
   record setup, actual readings, failures, and logs. Physical Bridge
   communication remains unverified.
5. Prepare Monday integration instructions for 2026-11-16 based on verified
   board/hardware availability. Do not prescribe unverified pin connections.
6. Before the 2026-11-15 23:59 IST deadline, update all five tracking documents,
   rerun the permitted offline suite once if source changes warrant it, record
   pending hardware tests, and produce the handover report.

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
- The CLI build passes; IDE GUI compilation, flashing, and physical operation
  remain unverified.
- MCU compilation passed for the UNO Q core; flashing and physical operation
  remain unverified. Expanded physical Bridge communication has not been tested.
- Watchdog configuration is **PENDING TIMING MEASUREMENTS**. Do not select or
  hardcode a timeout, enable the hardware watchdog, or introduce automatic
  watchdog resets. Feed policy requires essential-task success and user approval.
- Known blocking paths needing target measurements: `initializeIMU()` includes
  `delay(100)` and synchronous `Wire` calls; `readIMU()` uses synchronous I2C;
  `Serial.print` and `Bridge.call()` may block. Their maxima are NOT YET MEASURED.
- Hall speed, GPS, obstacle distance, and gyro acquisition are not established
  by the current telemetry sender; do not treat transmitted defaults as
  measurements.
- Current worktree changes are uncommitted. No change should be reverted,
  committed, or pushed without explicit user direction.
- The user confirmed the pending `Wire2`-to-`Wire` change in
  `firmware/mcu/src/imu.cpp` matches the actual wiring; physical sensor reads
  remain unverified.

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

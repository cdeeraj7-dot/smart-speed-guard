# Smart Speed Guard — Project Progress

Last verified checkpoint: 2026-11-15 (IST)

## Current phase

Stage 2 — MCU foundation (PARTIAL / IN PROGRESS). Stage 0's repository
inventory reconciliation and Stage 1's repository/build setup are complete.
The MCU loop now uses elapsed-time scheduling instead of a fixed 500 ms delay.
Hardware timing has been measured on the connected safe-bench UNO Q with
temporary instrumentation. Callback/CSV logging was rechecked after restarting
the receiver and restoring repository firmware; a separate receiver-app-stopped
MCU serial observation was also completed. Reset-to-setup timing,
Linux/Bridge service failure behavior, serial-failure behavior, I²C failure,
and recovery behavior remain unverified. Watchdog configuration is **PENDING
TIMING MEASUREMENTS** and explicitly deferred by the user. No timeout or feed
policy is selected.

Stage 2 acceptance is limited to MCU foundation evidence. Stage 3 sensor
interface validation, Stage 4 calibration/filtering, and Stage 5
safety-threshold approval are separate requirements and are not substitutes for
Stage 2 completion.

Observed timing values are summarized in
[firmware/mcu/README.md](./firmware/mcu/README.md). These are measured maxima
for a bounded sample, not guaranteed execution bounds. Repeated 16-field
callbacks and CSV logging were observed, including after an App Lab restart;
reset timing, Linux/Bridge service failure independence, serial failure, I²C
failure behavior, and recovery timing remain **NOT YET VERIFIED**.

The current engineering work is at an early MCU/sensor and telemetry bring-up
stage. It is not a completed hardware integration phase.

## Completed phases and verified outcomes

- Stage 0 architecture audit: repository inventory reconciled to the current
  source tree; technical board/electrical/protocol decisions remain unresolved.
- Stage 1 repository/build setup: Arduino CLI sketch entry and build
  instructions added; compile succeeded for `arduino:zephyr:unoq` with core
  1.0.0, CLI 1.5.1, and RouterBridge 0.4.3.
- Python test suite: 111 passed on 2026-11-14.
- Python syntax check (`compileall` for `ai`, `firmware`, and `tests`) passed on
  2026-11-14.
- Offline verification baseline (2026-11-14): Python suite 111 passed in
  0.56s; compileall passed; UNO Q CLI build passed (96,396 bytes program,
  40,984 bytes globals).
- No implementation phase has been accepted as fully complete based on these
  checks alone.
- UNO Q safe-bench profiling on 2026-11-15: `setup()` 123,874 us,
  `Bridge.begin()` 3 us, `initializeIMU()` 100,240 us. Across 780 profiled
  cycles, observed maxima were `readIMU()` 260 us, serial output 2,217 us,
  `Bridge.call()` 84,350 us, and full cycle 86,629 us. Instrumentation
  overhead was not measured. Callback delivery and CSV logging were verified
  in the initial run and rechecked after restarting App Lab and restoring the
  repository firmware.
- The diagnostic profile was removed after measurement. The normal repository
  firmware compiled and uploaded successfully, and its startup output reported
  `MPU6050 initialized` with subsequent accelerometer samples marked valid.
- The App Lab receiver logged the current 16-field callback and a displayed
  CSV snapshot with the expected header and 35 data rows. With that Python app
  stopped, a host serial sample showed 11 local MCU lines in 5.07 s at about
  500 ms intervals. App Lab Stop also stopped the MCU, so it was not a
  Linux-only failure injector; the Linux Bridge service was not isolated.

## Pending phases

See [PHASE_CHECKLIST.md](./PHASE_CHECKLIST.md) for all 21 development stages,
tasks, acceptance criteria, test status, and approval dependencies.

Current gates include:

- Verify board/toolchain/domain interfaces from authoritative sources.
- Measure actual startup, initialization, loop and blocking-operation durations
  on attached UNO Q hardware under normal and failure workloads. Initial
  safe-bench timing values are recorded; reset-to-setup and failure workloads
  remain pending.
- Establish that Linux/Bridge failure cannot starve MCU safety operation.
- Extend the current-schema callback/CSV checks with additional runs and
  controlled Linux/Bridge service failure and recovery tests.
- Keep watchdog disabled until timing results are recorded and the proposed
  timeout/feed policy is approved.
- Establish and test sensor interfaces with verified electrical details.
- Specify, test, and physically verify the full MCU/Linux message contract.
- Complete hardware, offline/recovery, and end-to-end testing.
- Do not infer sensor readings for sensors whose acquisition is not implemented.

## Current priorities

1. Measure reset-to-setup timing and controlled I²C/Bridge failure workloads.
   Watchdog configuration remains PENDING TIMING MEASUREMENTS and requires user
   approval after a proposal.
2. Keep electrical, transport, and hardware claims marked unverified
   until supported by authoritative sources or tests.
3. Arrange controlled checks for sensor validity/failure and MCU-only safety
   operation.

## Deadline status

The supplied deadline is 2026-11-15 23:59 IST. Safe-bench timing,
callback/CSV observations before and after receiver restart, and a
receiver-app-stopped serial sample were recorded on the UNO Q on 2026-11-15.
Full Linux/Bridge service failure, reset-to-setup timing, and I²C failure
tests remain outstanding. The earlier offline suite result (111 passed)
remains from 2026-11-14; no Python source was changed in this checkpoint.

## Source and device checkpoint

The worktree already contained uncommitted changes at this checkpoint; they are
preserved. The timing instrumentation was temporary and has been removed;
`firmware/mcu/src/main.cpp` is unchanged. The normal source build was compiled
and uploaded to the board over USB `COM5` after the profile run. No commit or
push was made.

Arduino App Lab 0.12.0 `Telemetry Receiver Test` contains the user-pasted
current receiver source and was running at the last observation. After App Lab
Run, the normal repository firmware was restored over `COM5` (the first flash
attempt timed out; the retry succeeded). Fresh callback logs resumed, with
distinct timestamps observed through 250,097 ms. The reopened CSV view showed
31 visible data rows with 16 fields each, spanning 232,093–247,096 ms; a
complete file row count was not established. The earlier receiver-app-stopped
serial sample remains a separate observation; App Lab Stop also stopped the
MCU. The separate `Smart Speed Guard MCU` app still has a `Hello world!`
Python entry point and stale `Wire2` code.

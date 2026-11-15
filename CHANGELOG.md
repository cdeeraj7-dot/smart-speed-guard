# Changelog

Important project changes only. This file does not imply that hardware
verification has occurred.

## 2026-11-14

### Documentation

- Added persistent project progress, development history, recovery instructions,
  phase acceptance checklist, and changelog.
- Reconciled the architecture audit inventory with the current source tree,
  while retaining unresolved technical questions and hardware limitations.
- Recorded that the repository has partial MCU/Linux/AI/dashboard software;
  physical integration results remain unverified.
- Added the UNO Q Arduino sketch entry and documented CLI build workflow;
  compile passed for the installed UNO Q target.
- Replaced the MCU telemetry loop's fixed 500 ms delay with elapsed-time
  scheduling; physical cadence is not yet measured.
- Recorded actual timing and watchdog measurement gates; watchdog remains
  PENDING TIMING MEASUREMENTS and is not implemented or enabled.
- Recorded that the current environment detected no attached board, preventing
  actual MCU timing and Bridge-failure measurements.

## 2026-11-15

### MCU/Linux message contract and validation

- Documented the current 16-field MCU-to-Linux telemetry message contract and
  the exact field ordering used by the live Bridge callback and CSV schema.
- Added a Python-side validation helper for the current Bridge payload to catch
  schema drift before rows are logged.
- Added a focused regression test covering the present callback format and
  invalid payload rejection.

### Stage 2 boundary and validation plan

- Clarified the Stage 2 boundary: MCU foundation timing and failure-recovery
  evidence remain separate from Stage 3 sensor electrical validation, Stage 4
  calibration/filtering requirements, and Stage 5 safety-threshold tuning.
- Added a detailed safe-bench validation plan for reset timing, Linux/Bridge
  failure, serial failure, I²C failure, local MCU operation during outage, and
  recovery checks.
- Explicitly recorded that App Lab Stop is not a valid Linux-only failure
  injector because it also stops the MCU.

### Hardware timing and deployment status

- Collected safe-bench UNO Q timing measurements on 2026-11-15 with a temporary
  profile build, then restored the normal repository firmware. The recorded
  values are bounded-sample observations, not guaranteed timing limits.
- The user manually deployed the current Linux receiver into App Lab
  `Telemetry Receiver Test`; repeated 16-field callbacks and a CSV snapshot
  with the expected header and 35 data rows were verified.
- With the Python receiver stopped, the normal repository firmware produced
  11 local serial telemetry lines in 5.07 s at approximately 500 ms intervals.
  App Lab Stop also stopped the MCU, so this was not a Linux-only failure
  injection. Linux/Bridge service failure, failure-case call duration,
  reset-to-setup timing, and I²C failure remain unverified.
- Restarted the App Lab receiver and restored the repository firmware over
  `COM5` after an OpenOCD timeout on the first attempt; the retry succeeded.
  Fresh callbacks resumed, and a reopened CSV view showed 31 visible 16-field
  rows. This was not a full-file count or a Linux/Bridge failure test.
- Reiterated the last offline test baseline (111 passed on 2026-11-14); no
  Python source changed during this timing checkpoint.

## 2026-11-09

### Telemetry

- MCU telemetry clears accelerometer values when the current sensor read is
  invalid and carries a separate `gyro_valid` flag.
- The MCU Bridge payload and Linux receiver/CSV schema include `gyro_valid`
  while retaining the MCU timestamp.
- Physical Bridge communication and MCU compilation remain unverified.

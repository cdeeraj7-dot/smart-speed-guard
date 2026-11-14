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
- Recorded the verified offline test result and outstanding hardware/toolchain
  verification.

## 2026-11-09

### Telemetry

- MCU telemetry clears accelerometer values when the current sensor read is
  invalid and carries a separate `gyro_valid` flag.
- The MCU Bridge payload and Linux receiver/CSV schema include `gyro_valid`
  while retaining the MCU timestamp.
- Physical Bridge communication and MCU compilation remain unverified.

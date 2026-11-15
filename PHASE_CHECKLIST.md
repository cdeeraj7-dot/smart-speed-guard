# Smart Speed Guard — Phase Checklist

Status definitions: **COMPLETE** means the stated acceptance criteria have
evidence; **PARTIAL** means some tasks exist but acceptance is incomplete;
**BLOCKED** means a dependency prevents safe progress; **NOT STARTED** means no
verified implementation is established. A passing software test does not imply
hardware validation.

Stage 2 scope boundary: Stage 2 covers MCU foundation only: startup timing,
initialization timing, loop cadence, diagnostics, Bridge/serial blocking
behavior, local safety operation without Linux, and failure/recovery evidence.
It does not include Stage 3 sensor electrical validation, Stage 4 calibration
and filtering acceptance, or Stage 5 safety-threshold tuning and hysteresis
approval. Those later-stage requirements remain distinct evidence gates and must
not be treated as Stage 2 completion criteria.

| Stage | Tasks | Status | Acceptance criteria | Test status | Approval / dependency |
|---|---|---|---|---|---|
| 0. Architecture audit | Define platform, processing boundaries, safety authority, risks, and unresolved decisions; reconcile the audit with the live repository. | COMPLETE (inventory audit) | Audit reflects current source and identifies verified decisions and remaining `TODO: VERIFY` items. | Audit inventory updated on 2026-11-14; Python suite 111 passed and compileall passed earlier the same day. Hardware not tested. | Technical decisions remain open, but are documented as blockers rather than being guessed. |
| 1. Repository structure | Establish the required source/documentation layout and reproducible development setup. | COMPLETE (CLI build setup) | Required active modules are organized; build/test/dependency instructions are reproducible; no fake implementation files. | Python tests and manifest exist; Arduino CLI UNO Q compile passed with documented versions on 2026-11-14. | IDE GUI compile and physical operation remain unverified. |
| 2. MCU foundation | Establish MCU entry point, initialization, timing, diagnostics, watchdog/recovery, and independent local operation. | PARTIAL / IN PROGRESS | MCU builds on the verified target; startup, initialization, loop, and failure timing are measured; local safety continues without Linux/Bridge availability. Sensor interface validation, calibration, and safety-threshold tuning belong to later stages and do not satisfy Stage 2 by themselves. | UNO Q safe-bench profile on 2026-11-15: `setup()` 123,874 us; `Bridge.begin()` 3 us; `initializeIMU()` 100,240 us. Across 780 cycles, observed maxima: `readIMU()` 260 us, serial output 2,217 us, `Bridge.call()` 84,350 us, cycle 86,629 us. A separate receiver-app-stopped sample showed 11 local serial lines in 5.07 s at ~500 ms intervals. Instrumentation overhead unmeasured; reset-to-setup, Linux/Bridge failure independence, serial failure, and I²C failure remain NOT YET VERIFIED. | Watchdog remains deferred. Stage 2 blockers are measured failure timing and evidence of local safety continuity under failed service or bus conditions; Stage 3/4/5 requirements are separate and not Stage 2 completion criteria. |
| 3. Sensor interfaces | Acquire Hall speed, HC-SR04 distance, GPS reference/location, and MPU6050 motion data. | PARTIAL | Each implemented interface has verified electrical connection, units, timing, validity, timeout, and error tests; Hall remains primary speed source. | IMU accelerometer returned valid samples in a safe-bench run; calibration, accuracy, electrical validation, and failure behavior are unverified. Other sensor acquisition is not established. | Exact board/module variants, wiring, electrical safety, and verified pin mapping. |
| 4. Filtering and calibration | Add sensor-specific filtering, calibration, freshness, and invalid/stale handling. | NOT STARTED / NEEDS AUDIT | Parameters and units are documented; invalid/stale data cannot appear as fresh; tests cover limits and recovery. | No phase acceptance evidence recorded. | Sensor sampling contracts and calibration/test fixtures. |
| 5. Deterministic safety engine | Implement approved overspeed, proximity, combined-risk, and impact rules with hysteresis where needed. | PARTIAL | Approved rules are deterministic, testable, and cannot be suppressed by AI/Linux. | `safety.cpp` is present; thresholds and acceptance are not established. | Project approval of thresholds, units, and alert-state requirements; measurements. |
| 6. Buzzer/LED alert system | Implement alert states and non-blocking local buzzer/LED behavior. | PARTIAL | Each approved alert maps to local outputs; transitions and MCU-only operation are tested. | LED code exists; physical outputs and buzzer behavior unverified. | Verified output pins, electrical limits, and alert-state approval. |
| 7. MCU/Linux communication | Verify official UNO Q transport; define message fields/order, version, timestamps, sequence/error recovery; implement both ends. | PARTIAL | Message contract and failure behavior are documented and tested on target hardware; MCU safety continues on Linux loss. | Repeated current 16-field callbacks were observed in two App Lab runs; `Bridge.call()` normal-case duration was profiled. A receiver-app-stopped serial sample showed later MCU cycles, but Linux/Bridge service failure and failure-case call duration remain unverified. | Verify official transport/runtime and current board/toolchain; test actual Linux/Bridge service failure and recovery. |
| 8. Linux service | Implement service startup, health reporting, restart/failure behavior, and resource boundaries. | PARTIAL | Service behavior is reproducible and failure isolation is tested. | The Python receiver ran and logged callbacks, including after restart; lifecycle/recovery is not verified. App Lab Stop also stopped the MCU, so it is not a Linux-only failure injector. | UNO Q Linux runtime and deployment requirements. |
| 9. Data logging | Log telemetry/events with timestamp, validity, connectivity, schema, and recovery behavior. | PARTIAL | Schema is versioned/documented; records preserve source timestamps and validity; write/recovery paths are tested. | The original `telemetry.csv` snapshot had 35 data rows; a reopened view after restart showed 31 visible data rows, all with 16 fields. This is not a full-file count; ongoing write/recovery behavior is not verified. | Approve retention and storage requirements; verify deployed filesystem behavior. |
| 10. AI dataset pipeline | Define dataset schema/preprocessing/features and validate offline processing. | PARTIAL | Schema, preprocessing, feature extraction, data validation, and measurable evaluation plan are documented and tested. | AI pipeline modules exist; current Python suite includes related tests. | Dataset provenance, labels, consent, and evaluation criteria. |
| 11. AI model development | Train/evaluate/version models without asserting unmeasured performance. | NOT STARTED / NEEDS AUDIT | Dataset and evaluation plan approved; offline metrics and model version/reproducibility recorded. | No model acceptance evidence recorded. | Validated dataset, labels, metrics, and resource targets. |
| 12. Edge AI inference | Deploy suitable inference as a non-authoritative enhancement. | NOT STARTED | On-device inference, resource use, failure handling, and deterministic safety independence are tested. | No edge inference validation recorded. | Model approval and verified UNO Q 2GB runtime capacity. |
| 13. Backend | Define and implement telemetry/event APIs and security boundaries. | NOT STARTED | API contract, auth, validation, error handling, and offline behavior are tested. | No backend acceptance evidence recorded. | Provider/deployment, data contract, credentials policy, and privacy approval. |
| 14. Database | Define schema, retention, migrations, and recovery. | NOT STARTED | Data model and migration/backup/recovery behavior are tested against requirements. | No database acceptance evidence recorded. | Backend and retention requirements. |
| 15. Dashboard | Visualize current/history telemetry, location, alerts, connectivity, and events. | PARTIAL | Required views consume defined APIs and handle stale/disconnected data clearly. | `dashboard/app.py` exists; end-to-end/API acceptance is not established. | User roles, views, accessibility, and data freshness requirements. |
| 16. LTE emergency system | Select/verify modem and implement emergency notification/fallback policy. | NOT STARTED | Exact modem and network behavior are verified; emergency path is tested with documented limits. | No modem/hardware verification recorded. | User-approved emergency policy and exact selected modem/network. |
| 17. Offline/recovery handling | Handle sensor, Linux, AI, Wi-Fi, cloud, LTE, and transport failures. | NOT STARTED / NEEDS AUDIT | Failure matrix and recovery tests show local deterministic alerts remain operational. | No complete failure-matrix results recorded. | Defined system interfaces and hardware/software fixtures. |
| 18. Full integration | Integrate MCU, Linux, AI, logging, backend, and dashboard. | NOT STARTED | End-to-end requirements pass in a reproducible environment, with offline behavior covered. | No full integration evidence recorded. | Prior phase acceptance and available integrated hardware/services. |
| 19. Testing and validation | Run unit, simulation, bench, hardware, and controlled field tests; report each distinctly. | PARTIAL | Acceptance results are reproducible; physical claims cite actual measurements; unmeasured values say `NOT YET MEASURED`. | Python: 111 passed; compileall passed. Safe-bench timing, two callback/CSV observations, and receiver-app-stopped local serial sample completed 2026-11-15; Linux/Bridge service failure, reset/I²C failure, broader system, and field tests remain unverified. | Test plans, verified hardware, equipment, safety review, and access. |
| 20. Documentation | Maintain architecture, hardware, protocol, testing, recovery, and handover documents. | PARTIAL | Documents agree with implementation, disclose unknowns/results, and permit a new session to resume. | Five persistent tracking documents created; audit inventory reconciled; hardware/protocol documentation still incomplete. | Verified technical decisions and phase test evidence. |

## Current checkpoint gates

- Stage 0 and Stage 1 are complete; Stage 2 has compile-verified cadence,
  measured normal-case timing, callback/CSV checks before and after receiver
  restart, and a receiver-app-stopped local serial sample. Reset timing,
  Linux/Bridge service failure, and controlled I²C failure remain unverified.
  Watchdog configuration is PENDING TIMING MEASUREMENTS and user approval; do
  not enable or feed a watchdog.
- Latest offline validation on 2026-11-14: 111 Python tests passed and
  `compileall` passed. On 2026-11-15 the profile build and normal UNO Q build
  compiled; the normal build was uploaded and startup output observed.
- The App Lab receiver contains the current source and was running at the last
  observation. Its Stop action also halts the MCU; App Lab Run flashes its own
  sketch, so re-upload repository firmware after running it.
- Callback logging was rechecked after restart. A reopened CSV view showed 31
  visible 16-field rows, but a full-file count was not established. Do not
  generalize these checks to Linux outage handling, sensor accuracy, or overall
  system validation.
- The 2026-11-15 handover records the offline-suite result and pending hardware
  tests; Monday integration instructions remain in `NEXT_SESSION.md`.

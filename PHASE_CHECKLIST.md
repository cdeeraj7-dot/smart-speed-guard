# Smart Speed Guard — Phase Checklist

Status definitions: **COMPLETE** means the stated acceptance criteria have
evidence; **PARTIAL** means some tasks exist but acceptance is incomplete;
**BLOCKED** means a dependency prevents safe progress; **NOT STARTED** means no
verified implementation is established. A passing software test does not imply
hardware validation.

| Stage | Tasks | Status | Acceptance criteria | Test status | Approval / dependency |
|---|---|---|---|---|---|
| 0. Architecture audit | Define platform, processing boundaries, safety authority, risks, and unresolved decisions; reconcile the audit with the live repository. | COMPLETE (inventory audit) | Audit reflects current source and identifies verified decisions and remaining `TODO: VERIFY` items. | Audit inventory updated on 2026-11-14; Python suite 111 passed and compileall passed earlier the same day. Hardware not tested. | Technical decisions remain open, but are documented as blockers rather than being guessed. |
| 1. Repository structure | Establish the required source/documentation layout and reproducible development setup. | COMPLETE (CLI build setup) | Required active modules are organized; build/test/dependency instructions are reproducible; no fake implementation files. | Python tests and manifest exist; Arduino CLI UNO Q compile passed with documented versions on 2026-11-14. | IDE GUI compile and physical operation remain unverified. |
| 2. MCU foundation | Establish MCU entry point, initialization, timing, diagnostics, watchdog/recovery, and independent local operation. | IN PROGRESS / TIMING BLOCKED | MCU builds on the verified target; startup/failure behavior and timing are measured; local safety does not depend on Linux. | UNO Q compile passed; elapsed-time scheduling present. Actual startup/init/loop maxima, Bridge-failure independence, and hardware behavior NOT YET MEASURED. | Watchdog is PENDING TIMING MEASUREMENTS. Measure on hardware, propose timeout/feed policy, and obtain user approval before implementation. |
| 3. Sensor interfaces | Acquire Hall speed, HC-SR04 distance, GPS reference/location, and MPU6050 motion data. | PARTIAL | Each implemented interface has verified electrical connection, units, timing, validity, timeout, and error tests; Hall remains primary speed source. | IMU accelerometer implementation exists; physical acquisition unverified. Other sensor acquisition is not established. | Exact board/module variants, wiring, electrical safety, and verified pin mapping. |
| 4. Filtering and calibration | Add sensor-specific filtering, calibration, freshness, and invalid/stale handling. | NOT STARTED / NEEDS AUDIT | Parameters and units are documented; invalid/stale data cannot appear as fresh; tests cover limits and recovery. | No phase acceptance evidence recorded. | Sensor sampling contracts and calibration/test fixtures. |
| 5. Deterministic safety engine | Implement approved overspeed, proximity, combined-risk, and impact rules with hysteresis where needed. | PARTIAL | Approved rules are deterministic, testable, and cannot be suppressed by AI/Linux. | `safety.cpp` is present; thresholds and acceptance are not established. | Project approval of thresholds, units, and alert-state requirements; measurements. |
| 6. Buzzer/LED alert system | Implement alert states and non-blocking local buzzer/LED behavior. | PARTIAL | Each approved alert maps to local outputs; transitions and MCU-only operation are tested. | LED code exists; physical outputs and buzzer behavior unverified. | Verified output pins, electrical limits, and alert-state approval. |
| 7. MCU/Linux communication | Verify official UNO Q transport; define message fields/order, version, timestamps, sequence/error recovery; implement both ends. | PARTIAL | Message contract and failure behavior are documented and tested on target hardware; MCU safety continues on Linux loss. | Existing Bridge reference is accelerometer-only; expanded payload/receiver code exists but physical operation is NOT YET MEASURED. | Verify official transport/runtime and current board/toolchain. |
| 8. Linux service | Implement service startup, health reporting, restart/failure behavior, and resource boundaries. | PARTIAL | Service behavior is reproducible and failure isolation is tested. | Python receiver exists; service lifecycle/recovery is not verified. | UNO Q Linux runtime and deployment requirements. |
| 9. Data logging | Log telemetry/events with timestamp, validity, connectivity, schema, and recovery behavior. | PARTIAL | Schema is versioned/documented; records preserve source timestamps and validity; write/recovery paths are tested. | Receiver CSV callback/schema can be unit exercised; physical data path unverified. | Approve retention and storage requirements; verify deployed filesystem behavior. |
| 10. AI dataset pipeline | Define dataset schema/preprocessing/features and validate offline processing. | PARTIAL | Schema, preprocessing, feature extraction, data validation, and measurable evaluation plan are documented and tested. | AI pipeline modules exist; current Python suite includes related tests. | Dataset provenance, labels, consent, and evaluation criteria. |
| 11. AI model development | Train/evaluate/version models without asserting unmeasured performance. | NOT STARTED / NEEDS AUDIT | Dataset and evaluation plan approved; offline metrics and model version/reproducibility recorded. | No model acceptance evidence recorded. | Validated dataset, labels, metrics, and resource targets. |
| 12. Edge AI inference | Deploy suitable inference as a non-authoritative enhancement. | NOT STARTED | On-device inference, resource use, failure handling, and deterministic safety independence are tested. | No edge inference validation recorded. | Model approval and verified UNO Q 2GB runtime capacity. |
| 13. Backend | Define and implement telemetry/event APIs and security boundaries. | NOT STARTED | API contract, auth, validation, error handling, and offline behavior are tested. | No backend acceptance evidence recorded. | Provider/deployment, data contract, credentials policy, and privacy approval. |
| 14. Database | Define schema, retention, migrations, and recovery. | NOT STARTED | Data model and migration/backup/recovery behavior are tested against requirements. | No database acceptance evidence recorded. | Backend and retention requirements. |
| 15. Dashboard | Visualize current/history telemetry, location, alerts, connectivity, and events. | PARTIAL | Required views consume defined APIs and handle stale/disconnected data clearly. | `dashboard/app.py` exists; end-to-end/API acceptance is not established. | User roles, views, accessibility, and data freshness requirements. |
| 16. LTE emergency system | Select/verify modem and implement emergency notification/fallback policy. | NOT STARTED | Exact modem and network behavior are verified; emergency path is tested with documented limits. | No modem/hardware verification recorded. | User-approved emergency policy and exact selected modem/network. |
| 17. Offline/recovery handling | Handle sensor, Linux, AI, Wi-Fi, cloud, LTE, and transport failures. | NOT STARTED / NEEDS AUDIT | Failure matrix and recovery tests show local deterministic alerts remain operational. | No complete failure-matrix results recorded. | Defined system interfaces and hardware/software fixtures. |
| 18. Full integration | Integrate MCU, Linux, AI, logging, backend, and dashboard. | NOT STARTED | End-to-end requirements pass in a reproducible environment, with offline behavior covered. | No full integration evidence recorded. | Prior phase acceptance and available integrated hardware/services. |
| 19. Testing and validation | Run unit, simulation, bench, hardware, and controlled field tests; report each distinctly. | PARTIAL | Acceptance results are reproducible; physical claims cite actual measurements; unmeasured values say `NOT YET MEASURED`. | Python: 111 passed; compileall passed. MCU, physical Bridge, bench, and field tests unverified. | Test plans, verified hardware, equipment, safety review, and access. |
| 20. Documentation | Maintain architecture, hardware, protocol, testing, recovery, and handover documents. | PARTIAL | Documents agree with implementation, disclose unknowns/results, and permit a new session to resume. | Five persistent tracking documents created; audit inventory reconciled; hardware/protocol documentation still incomplete. | Verified technical decisions and phase test evidence. |

## Current checkpoint gates

- Stage 0 and Stage 1 are complete; Stage 2 has one compile-verified loop
  cadence increment. Actual timing and Bridge-failure behavior remain
  unmeasured. Watchdog configuration is PENDING TIMING MEASUREMENTS and user
  approval; do not enable or feed a watchdog.
- Latest offline validation on 2026-11-14: 111 Python tests passed,
  `compileall` passed, UNO Q CLI compile passed, and `git diff --check` passed.
  No board was attached, so no physical timing was measured.
- Keep all six pre-existing uncommitted source files intact; inspect their diffs
  before further edits.
- Do not mark the expanded Bridge path, MCU build, or physical sensors verified
  without target testing.
- Before the 2026-11-15 deadline, record the offline-suite result, list pending
  hardware tests, and prepare Monday integration instructions.

# Smart Speed Guard — Architecture Audit

## 1. Repository Status

Audit basis:

- `AGENTS.md` is present at the repository root and is the authoritative project instruction file.
- `README.md` is present and contains only the project title and a short description.
- No application source code is present.
- No MCU firmware is present.
- No Linux service is present.
- No AI/ML pipeline or model is present.
- No backend, database, dashboard, or cloud integration is present.
- No LTE integration is present.
- No simulation files are present.
- No test suite, test fixtures, build configuration, dependency manifest, environment template, or CI configuration is present.
- No hardware pin map, wiring diagram, protocol specification, sensor calibration record, or measured validation result is present.

Current state: repository setup only. Stage 0 architecture audit is not an implementation baseline. There is no executable system to build or validate, and no performance result is available. Any unmeasured metric must remain `NOT YET MEASURED`.

The proposed repository structure in `AGENTS.md` is suitable as a staged target. It should be created incrementally as each development stage begins rather than as empty placeholder directories.

## 2. Current Architecture

The authoritative Phase-2 platform is Arduino UNO Q 2GB with two processing domains:

1. **STM32U585 real-time MCU:** deterministic acquisition, low-level interfacing, timing-sensitive processing, basic filtering, deterministic safety decisions, local alerts, watchdog/recovery, and continued safety operation during Linux or network failure.
2. **Qualcomm QRB2210 Linux:** higher-level processing, AI/ML inference, appropriate sensor fusion, logging, analytics, cloud/backend communication, dashboard-related services, and non-safety-critical configuration.

The safety boundary is clear: deterministic MCU logic is authoritative for hard safety triggers. Linux and AI may enrich, classify, log, or recommend, but must never suppress or override a deterministic trigger.

The architecture is internally consistent at the responsibility level. The following boundaries are not yet implementable because they are unspecified:

- `TODO: VERIFY` the exact UNO Q board variant, official processing-domain interfaces, supported development toolchain, and available operating-system/runtime versions.
- `TODO: VERIFY` which domain directly owns each physical sensor and actuator.
- `TODO: VERIFY` the MCU-to-Linux transport and its electrical and software interfaces.
- `TODO: VERIFY` the timing, freshness, and validity contract for data crossing the domain boundary.
- `TODO: VERIFY` how configuration is provisioned while preserving MCU operation without Linux.

## 3. Hardware Architecture

Declared hardware:

- Arduino UNO Q 2GB
- NEO-6M GPS
- HC-SR04 ultrasonic sensor
- A3144 Hall-effect sensor
- MPU6050 accelerometer/gyroscope
- Active buzzer
- LED
- Wi-Fi
- 4G/LTE cellular/SIM communication module
- Automotive 12V input with appropriate automotive-rated buck conversion and power protection

No pin assignments are defined. Old ESP32 mappings must not be reused.

Required hardware verification before implementation:

- `TODO: VERIFY` the exact UNO Q board documentation and available headers/interfaces.
- `TODO: VERIFY` voltage, current, logic-level, grounding, and protection requirements for every module.
- `TODO: VERIFY` the actual power budget, startup behavior, brownout behavior, reset behavior, and protection strategy from the 12V automotive input.
- `TODO: VERIFY` whether each sensor is electrically compatible with the selected MCU interface.
- `TODO: VERIFY` Hall sensor supply, output type, pull-up requirements, signal conditioning, and mounting arrangement.
- `TODO: VERIFY` GPS supply, logic levels, interface, antenna, and time-to-first-fix expectations.
- `TODO: VERIFY` MPU6050 bus mode, address, voltage levels, pull-ups, interrupt usage, mounting orientation, and calibration procedure.
- `TODO: VERIFY` HC-SR04 trigger and echo voltage levels, level-shifting or protection circuit, maximum usable range, and transducer mounting. A potentially 5V ECHO signal must not be connected directly to a 3.3V-only input.
- `TODO: VERIFY` buzzer and LED drive current, required transistor or driver, polarity, and failure behavior.
- `TODO: VERIFY` Wi-Fi antenna, network provisioning, and availability assumptions.
- `TODO: VERIFY` the LTE modem model, power supply/transient requirements, antenna, SIM requirements, interface, supported networks, and regulatory/network availability.

The design must not directly control brakes, steering, throttle, the engine ECU, or safety-critical CAN functions.

## 4. MCU Responsibilities

The MCU should own the minimum safety path required for continued local operation:

- Sensor acquisition for safety-critical inputs, subject to verified interface ownership.
- Timestamping and validity checks.
- Hall pulse measurement and primary speed calculation.
- Proximity measurement and filtering where the MCU owns the HC-SR04 interface.
- Basic IMU processing required for deterministic event indicators.
- Deterministic overspeed, proximity, combined-risk, and implemented severe-event rules.
- Hysteresis and alert-state transitions.
- Local buzzer and LED control through non-blocking scheduling/state machines.
- Watchdog and recovery behavior.
- A bounded, validated data contract to Linux.
- Local operation when Linux, AI, Wi-Fi, cloud, or LTE services fail.

Required MCU design decisions:

- `TODO: VERIFY` MCU firmware framework, compiler, linker/build process, startup code, and debug/programming method.
- `TODO: VERIFY` interrupt/timer resources and safe pulse-capture mechanism for the Hall sensor.
- `TODO: VERIFY` sampling rates, execution deadlines, worst-case latency, and watchdog timeout.
- `TODO: VERIFY` fixed-point versus floating-point requirements and resource budget.
- `TODO: VERIFY` threshold source, configuration range, persistence, and safe defaults.
- `TODO: VERIFY` behavior for stale, missing, out-of-range, or contradictory sensor data.
- `TODO: VERIFY` alert-level definitions, transition hysteresis, latching, acknowledgement, and reset behavior.

No MCU implementation currently exists.

## 5. Linux Responsibilities

The Linux side should provide non-safety-critical services:

- Receive validated MCU data and health status.
- Perform higher-level processing and sensor fusion where appropriate.
- Run AI/ML inference without authority to suppress deterministic MCU alerts.
- Log raw or appropriately summarized telemetry and events.
- Provide analytics and model/data version metadata.
- Manage cloud/backend communication over Wi-Fi as the normal telemetry path.
- Coordinate the LTE emergency/fallback service after the modem and policy are verified.
- Provide dashboard-facing APIs or data services.
- Manage non-safety-critical configuration and service health.

Linux must degrade independently. A Linux crash, service timeout, AI failure, Wi-Fi loss, cloud outage, or LTE outage must not stop the MCU safety path.

Required Linux decisions:

- `TODO: VERIFY` Linux distribution, runtime versions, service manager, resource limits, storage availability, and update strategy.
- `TODO: VERIFY` whether Linux can access sensors directly or must receive all sensor data from the MCU.
- `TODO: VERIFY` process boundaries, restart policy, local queueing, and log rotation.
- `TODO: VERIFY` whether dashboard access is local, remote, cloud-mediated, or all three.

No Linux implementation currently exists.

## 6. Sensor Data Flow

The intended logical data flow is:

1. A3144 Hall pulses are acquired with MCU-appropriate timing mechanisms.
2. The MCU converts pulse timing or counts into wheel rotational speed and vehicle speed using calibrated wheel circumference and pulses per revolution.
3. NEO-6M supplies supplementary speed, position, and time data for cross-checking and geographic logging.
4. HC-SR04 supplies forward distance measurements through a non-blocking, electrically protected interface.
5. MPU6050 supplies calibrated acceleration and angular-rate data for braking, acceleration, abnormal-motion, impact-related, and AI features.
6. The MCU validates and filters safety-relevant data, computes deterministic rules, and drives local alerts.
7. A documented MCU-Linux interface transfers bounded telemetry, event, health, and status data to Linux.
8. Linux logs data, performs higher-level analysis/AI, communicates with backend services, and supports dashboard views.

Acquisition and processing requirements:

- Hall: pulse counting/timing, debouncing or signal conditioning as appropriate, zero-speed timeout, wheel circumference calibration, pulses-per-revolution calibration, outlier handling, and configurable filtering.
- GPS: serial/bus framing validation, fix validity, timestamp handling, position validity, speed cross-check policy, unavailable-fix behavior, and no automatic replacement of Hall speed without an explicit documented architecture change.
- Ultrasonic: non-blocking trigger/measurement scheduling, timeout handling, invalid echo handling, electrical protection, plausibility bounds, filtering, and stale-data policy.
- IMU: bus error handling, calibration, axis/orientation definition, bias management, sampling, filtering, saturation/invalid data detection, and event-window buffering.

`TODO: VERIFY` all sampling frequencies, filter types and parameters, calibration procedures, timestamps, units, coordinate frames, maximum tolerable age, and data-quality flags. No sensor data path is implemented.

## 7. Safety Architecture

The system is an academic monitoring and alerting prototype. It warns the driver and reports events; it does not actuate vehicle control systems.

The deterministic MCU safety engine should define testable rules for:

- Overspeed relative to a configurable speed threshold.
- Unsafe proximity relative to a configurable distance or speed-dependent policy.
- Combined speed and proximity risk, potentially using stopping-distance or time-to-collision concepts only after the required assumptions are defined and validated.
- Severe impact or accident indicators where implemented, using IMU and other available evidence without claiming perfect collision prediction.

The safety engine requires:

- Explicit input validity and stale-data handling.
- Configurable thresholds with documented units and safe bounds.
- Hysteresis to prevent alert chatter where appropriate.
- Deterministic alert states and transition rules.
- Non-blocking execution and bounded processing time.
- Local operation independent of Linux and AI.
- Event records containing sufficient timestamp, source, and state information for later diagnosis.

`TODO: VERIFY` the speed limit source, distance thresholds, units, stopping-policy assumptions, alert levels, hysteresis values, event latching, recovery rules, and acceptable false-alert/missed-alert tradeoffs. Thresholds, latency, accuracy, and detection performance are `NOT YET MEASURED`.

## 8. AI Architecture

AI is an enhancement layer only. It may support:

- Driving-behavior classification.
- Anomaly detection.
- Sensor-fusion or risk scoring.
- Event classification.
- Historical telemetry analysis.

AI must not suppress, downgrade, delay, or override a hard deterministic MCU safety trigger. AI failure, model absence, inference timeout, invalid output, or Linux failure must leave deterministic safety behavior unchanged.

Before model development:

- Define the dataset schema, units, timestamps, labels, and provenance.
- Define preprocessing and feature engineering.
- Separate training, validation, test, and inference workflows.
- Define measurable evaluation metrics and acceptance criteria.
- Record model and dataset versions.
- Define resource, latency, storage, and update limits for the UNO Q 2GB configuration.
- Test offline and against invalid, missing, delayed, and out-of-distribution data.

`TODO: VERIFY` the initial AI use case, labels, dataset source and consent/provenance, feature set, model family, runtime, model-update policy, resource budget, inference deadline, and fallback behavior. Accuracy and successful inference are `NOT YET MEASURED`.

No AI code or model is present.

## 9. Cloud and Backend Architecture

The eventual backend should support authenticated ingestion and retrieval of:

- Vehicle telemetry.
- Speed and obstacle distance.
- GPS position and timestamps.
- Alert level and event history.
- IMU/event information.
- Connectivity status.
- Important and emergency events.

Normal telemetry should primarily use Wi-Fi. Critical events may use LTE fallback after modem and communication policy verification. Local buffering should support later upload when connectivity returns.

Required backend decisions:

- `TODO: VERIFY` backend platform, API style, payload schema, units, timestamps, authentication, authorization, retention, database technology, deployment model, and availability requirements.
- `TODO: VERIFY` ordering, deduplication, replay protection, idempotency, rate limits, and payload-size limits.
- `TODO: VERIFY` whether location and telemetry require privacy controls, consent, access logging, redaction, or retention limits.

Credentials and private material must be supplied through protected configuration/environment mechanisms and never hard-coded or committed. No cloud, backend, database, or endpoint currently exists.

## 10. LTE Emergency Architecture

LTE is intended primarily for emergency communication, critical-event notification, GPS-tagged emergency SMS, possible emergency calling if supported by the selected modem/network, and critical-event fallback when Wi-Fi is unavailable.

The emergency path should be subordinate to local deterministic alerting: a modem or network failure must not disable the buzzer, LED, or MCU safety rules.

Required emergency-path behavior to define:

- Event qualification and severity policy.
- Which data is transmitted and how location validity is represented.
- Retry, backoff, timeout, duplicate suppression, and acknowledgement policy.
- Local queueing and delivery status.
- Privacy, consent, recipient configuration, and rate limiting.
- Handling of no GPS fix, no SIM, no registration, no signal, modem reset, and power loss.
- Separation between emergency communication and normal telemetry.

`TODO: VERIFY` the exact LTE modem, network/operator support, SIM and subscription, antenna, power design, host interface, driver/library, command set, SMS/call support, emergency-contact policy, legal/regulatory constraints, and whether emergency calling is appropriate. No modem commands or interface are assumed.

## 11. Failure and Offline Behaviour

The architecture must tolerate:

- Wi-Fi loss.
- Cloud/backend unavailability.
- Linux service crash or restart.
- AI service failure or invalid inference.
- LTE unavailability.
- Sensor timeout or invalid reading.
- GPS unavailability.
- Corrupted, malformed, stale, duplicated, or out-of-order MCU/Linux messages.
- MCU/Linux communication timeout.
- Power interruption, brownout, or reset.
- Storage exhaustion or corrupted local logs.

Required behavior:

- MCU deterministic safety and local alerts continue without Linux or network services.
- Invalid or stale inputs are explicitly marked and cannot silently become valid safety data.
- Linux services restart or degrade without changing MCU safety decisions.
- Important events may be buffered locally and uploaded later with ordering and duplicate handling.
- Communication has timeouts, bounded queues, health status, and recovery procedures.
- Failure states are observable and testable.

`TODO: VERIFY` queue capacities, persistence medium, retention, recovery timing, watchdog ownership, reboot sequencing, clock behavior, and safe behavior for each sensor failure mode. No offline or recovery implementation exists.

## 12. Security

Security requirements include:

- No hard-coded passwords, API keys, tokens, SIM credentials, Wi-Fi credentials, or private certificates.
- Protected configuration and secret storage appropriate to the UNO Q platform.
- Authenticated and authorized backend access.
- Secure transport where supported and verified.
- Input validation for sensor, inter-domain, LTE, and network data.
- Message integrity, replay protection, and sequence/timeout handling for MCU-Linux communication.
- Least-privilege Linux services and restricted dashboard/API access.
- Safe logging that excludes secrets and limits sensitive location exposure.
- Controlled firmware, service, model, and configuration updates.
- Recovery behavior for malformed messages and compromised or unavailable services.

`TODO: VERIFY` available hardware-backed security facilities, secure boot/update capabilities, key provisioning, certificate lifecycle, local access controls, threat model, privacy requirements, network exposure, and acceptable security tradeoffs for the academic prototype. No security controls are implemented or validated.

## 13. Testing Strategy

Testing must distinguish design, implementation, simulation, bench testing, hardware testing, field testing, measured results, and expected results. Simulation is not physical validation. Unmeasured metrics are `NOT YET MEASURED`.

Planned test layers:

- Unit tests for pulse-to-speed conversion, filtering, plausibility checks, distance processing, IMU features, thresholds, hysteresis, and state transitions.
- MCU tests for timing, watchdog/recovery, alert outputs, invalid/stale sensor inputs, and deterministic operation without Linux.
- Protocol tests for message encoding/decoding, IDs, timestamps, sequence numbers, corruption, replay, timeout, version mismatch, and recovery.
- Linux service tests for process restart, logging, AI failure, queueing, backend failure, and resource limits.
- AI tests for preprocessing, offline inference, invalid inputs, versioning, metrics, latency, and fallback.
- Backend tests for authentication, schema validation, idempotency, ordering, storage, retention, failure, and recovery.
- LTE tests for registration failure, unavailable network, retry/backoff, duplicate suppression, invalid location, modem reset, and emergency policy.
- Hardware and integration tests for actual wiring, signal levels, power behavior, sensor calibration, alert outputs, and full data flow.
- Field tests only after safe bench validation and with documented procedures and risk controls.

`TODO: VERIFY` test equipment, fixtures, simulators, hardware availability, test data, acceptance criteria, fault-injection approach, logging format, and approval process. No tests or results currently exist.

## 14. Dependencies

Hardware dependencies:

- Verified Arduino UNO Q 2GB board and official documentation.
- Verified selected sensors and their datasheets.
- Electrical protection and level shifting for incompatible signals, especially HC-SR04 ECHO if applicable.
- Automotive-rated input protection and buck conversion.
- Selected LTE modem, SIM/service, antenna, and required host interface.
- Bench power, measurement equipment, safe sensor fixtures, and test wiring.

Software dependencies not yet selected:

- MCU toolchain and firmware framework.
- Linux distribution, language runtimes, service manager, and build tools.
- Sensor drivers and protocol libraries.
- AI runtime and model-development toolchain.
- Local storage/logging components.
- Backend, database, authentication, and dashboard technologies.
- LTE driver/library or verified modem integration layer.
- Test, simulation, static-analysis, and CI tools.

`TODO: VERIFY` every dependency version, license/academic-use suitability, maintenance status, platform compatibility, resource cost, and reproducible installation method before adoption. No dependencies are installed or declared.

## 15. Unverified Technical Decisions

The following decisions block or constrain implementation and must be resolved from official documentation, datasheets, the actual hardware, or an explicit project-team decision:

- `TODO: VERIFY` exact UNO Q 2GB board revision, available interfaces, and supported development workflow.
- `TODO: VERIFY` MCU and Linux physical/logical inter-domain communication mechanism.
- `TODO: VERIFY` all pin mappings; no pin number is currently authorized.
- `TODO: VERIFY` voltage levels, current limits, level shifting, pull-ups, grounding, and protection for every connection.
- `TODO: VERIFY` ownership of each sensor and actuator between MCU and Linux.
- `TODO: VERIFY` Hall pulse topology, wheel geometry, pulses per revolution, calibration, and zero-speed policy.
- `TODO: VERIFY` GPS interface, time source, fix-quality policy, and cross-check policy.
- `TODO: VERIFY` HC-SR04 electrical interface, scheduling, measurement limits, and filtering.
- `TODO: VERIFY` MPU6050 orientation, calibration, sampling, filtering, and event features.
- `TODO: VERIFY` alert states, thresholds, hysteresis, latching, and safe defaults.
- `TODO: VERIFY` MCU deadlines, sampling rates, watchdogs, memory, storage, and power budgets.
- `TODO: VERIFY` message format, IDs, versioning, timestamps, sequence numbers, integrity, and recovery.
- `TODO: VERIFY` Linux service boundaries, restart policy, and resource limits.
- `TODO: VERIFY` LTE hardware, modem commands, network support, emergency policy, and power behavior.
- `TODO: VERIFY` cloud/backend schema, security, retention, and availability requirements.
- `TODO: VERIFY` dashboard users, views, access model, and data freshness expectations.
- `TODO: VERIFY` AI scope, dataset, labels, metrics, runtime, model lifecycle, and fallback.
- `TODO: VERIFY` privacy, consent, threat model, and academic data-handling requirements.
- `TODO: VERIFY` test equipment, fixtures, acceptance criteria, and hardware-test access.

## 16. Missing Information

The project team must provide or approve:

- Exact UNO Q board documentation and the physical board revision available for development.
- Confirmed selected LTE modem and network/SIM plan.
- Intended physical mounting and wiring for every sensor, buzzer, LED, antenna, and power component.
- Vehicle or bench wheel dimensions, pulses per revolution, and calibration method.
- Required operating ranges, threshold policy, and intended alert semantics.
- Expected sampling, freshness, and latency requirements.
- Decision on which sensors are MCU-owned and what data Linux receives.
- Approved MCU-Linux transport after official verification.
- Configuration ownership and update/recovery process.
- AI use case, dataset plan, labels, and evaluation criteria.
- Backend/cloud provider or deployment constraints.
- Dashboard audience, access model, required screens, and retention period.
- Emergency-contact and LTE communication policy.
- Privacy, consent, threat-model, credential, and data-retention requirements.
- Available development, test, measurement, and hardware-validation resources.
- Definition of acceptance for each implementation stage.

Every missing board-specific, electrical, protocol, modem, performance, or safety detail remains `TODO: VERIFY` until resolved.

## 17. Recommended Implementation Order

The `AGENTS.md` staged order is suitable and should be followed with the following audit gates:

1. Complete this architecture audit and resolve the highest-risk `TODO: VERIFY` items.
2. Establish the repository structure and reproducible development/toolchain documentation without adding fake implementations.
3. Verify the UNO Q board, power design, signal levels, physical interfaces, and selected hardware.
4. Build the MCU foundation with watchdog, timing, diagnostics, configuration boundaries, and host-independent operation.
5. Implement and unit-test one sensor interface at a time, beginning with Hall speed, then proximity, GPS cross-checking, and IMU features as their hardware contracts are verified.
6. Implement filtering, calibration, validity, stale-data, and error handling with tests and explicit units.
7. Implement deterministic safety rules, alert states, hysteresis, and local buzzer/LED behavior.
8. Verify and implement the MCU-Linux protocol with message tests, timeout, corruption, version, and recovery behavior.
9. Implement the Linux service, logging, local buffering, and health monitoring.
10. Define the AI dataset and evaluation plan before model development; implement AI only as a non-authoritative enhancement.
11. Implement backend, database, dashboard, and normal Wi-Fi telemetry after their contracts are defined.
12. Select and verify the LTE modem and implement the emergency/fallback path with explicit policy and failure tests.
13. Complete offline/recovery handling, integration testing, bench testing, hardware testing, and only then controlled field testing.
14. Document measured results separately from simulations and expected behavior.

No stage should claim completion without executable validation appropriate to that stage.

## 18. Architecture Risks

Major risks identified:

- **Unverified hardware interfaces:** Incorrect voltage levels or pin assumptions could damage hardware or create unsafe measurements. Mitigation: official documentation, datasheets, electrical review, and verified level shifting before wiring.
- **Undefined MCU-Linux transport:** An invented or unsuitable transport could break determinism or failure isolation. Mitigation: verify the official mechanism and define a versioned, bounded protocol before implementation.
- **Unspecified sensor timing and calibration:** Speed, distance, and IMU outputs may be misleading without known sampling, filtering, calibration, and validity rules. Mitigation: define units, timing, calibration, and quality flags with tests.
- **Threshold and alert ambiguity:** Undocumented thresholds or hysteresis can cause false alerts, missed alerts, or chatter. Mitigation: project-team approval, deterministic state tables, and measured testing.
- **Power and automotive environment:** The 12V input may expose the system to transients, noise, brownouts, and resets. Mitigation: verified automotive-rated power protection and bench testing before vehicle use.
- **LTE uncertainty:** Modem, network, power, and emergency capabilities are unknown. Mitigation: select hardware first and verify the complete emergency path; do not assume commands or calling support.
- **AI authority creep:** AI could incorrectly influence safety behavior. Mitigation: enforce MCU deterministic authority and treat AI failure as non-safety-critical.
- **Cloud/network dependency:** Connectivity loss could cause data loss or incorrectly imply loss of safety. Mitigation: local safety, health state, bounded buffering, and later upload.
- **Privacy and security exposure:** GPS and emergency data are sensitive. Mitigation: define threat model, access control, secret management, retention, and consent before deployment.
- **Insufficient validation resources:** No tests, hardware fixtures, measurements, or acceptance criteria currently exist. Mitigation: plan unit, simulation, bench, hardware, and field validation separately.
- **Scope expansion before foundation:** Implementing AI, cloud, dashboard, or LTE before hardware and safety contracts are verified would create rework and unsupported claims. Mitigation: follow the staged order and audit gates.

## 19. Final Audit Verdict

The repository is correctly at the beginning of Stage 0. The declared Phase-2 architecture is conceptually consistent: the STM32U585 MCU owns deterministic local safety, while the Qualcomm QRB2210 Linux side owns higher-level, AI, logging, cloud, and dashboard functions. The non-control monitoring boundary and AI non-authority rule are appropriate and must be preserved.

However, the project is not implementation-ready for hardware or inter-domain software. No code, dependencies, pin map, wiring, protocol, selected LTE modem, calibration data, thresholds, test assets, or measured results exist. The highest-priority work is to resolve the `TODO: VERIFY` decisions concerning the actual UNO Q interfaces, electrical design, sensor ownership and timing, MCU-Linux transport, power behavior, and LTE hardware/policy.

Audit status: **Stage 0 architecture audit complete; implementation readiness: blocked pending verification of the identified technical decisions.**

No physical validation, performance result, successful inference, communication capability, or safety compliance claim is made by this document.

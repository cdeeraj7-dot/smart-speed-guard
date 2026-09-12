# AGENTS.md

## Project

Smart Speed Guard is an academic automotive safety monitoring and alerting system. The current authoritative Phase-2 computing platform is the Arduino UNO Q 2GB.

This repository instruction file governs all implementation, documentation, testing, and validation work. Build incrementally and do not fabricate technical facts, measurements, citations, validation, or test results.

## Current Phase-2 Architecture

The system has two processing domains:

### STM32U585 real-time MCU

The MCU is responsible for:

- Deterministic sensor acquisition and low-level interfacing
- Timing-sensitive processing and basic filtering
- Deterministic safety threshold logic
- Local alert generation and buzzer/LED control
- Watchdog and recovery functions
- Safety operation when Linux, AI, cloud, or network services fail

### Qualcomm QRB2210 Linux

The Linux side is responsible for:

- Higher-level processing
- AI/ML inference
- Sensor fusion where appropriate
- Data logging and analytics
- Cloud/backend communication
- Dashboard-related functions
- Configuration and non-safety-critical services

The MCU safety path must remain functional when Linux, AI, Wi-Fi, cloud services, or LTE fail. AI augments the deterministic safety system and must never suppress or override a hard deterministic safety trigger.

The authoritative memory configuration is 2GB. Do not design assuming 4GB RAM.

## Current Hardware

The current hardware is:

- Arduino UNO Q 2GB
- NEO-6M GPS
- HC-SR04 ultrasonic sensor
- A3144 Hall-effect sensor
- MPU6050 accelerometer/gyroscope
- Active buzzer
- LED
- Wi-Fi
- 4G/LTE cellular/SIM communication module
- Automotive 12V input
- Appropriate automotive-rated buck conversion and power protection

The LTE module is intended primarily for emergency communication, critical-event notification, GPS-tagged emergency SMS, possible emergency calling if supported by the selected modem/network, and critical-event fallback when Wi-Fi is unavailable. Normal telemetry and cloud reporting should primarily use Wi-Fi.

The exact LTE modem model is not fixed. Do not invent its interface, commands, voltage requirements, UART pins, USB configuration, or AT-command set.

## Hardware Pins and Electrical Safety

Do not reuse old ESP32 GPIO assignments. Any UNO Q pin mapping must be based on official UNO Q documentation, the actual board available to the user, verified electrical requirements, and the exact selected peripheral/module.

Until verified, represent unknown mappings exactly as:

`TODO: VERIFY PIN MAPPING`

Never invent a pin number. HC-SR04 ECHO may be a 5V signal; never connect a potentially 5V ECHO output directly to a 3.3V-only input without verified level shifting or interface protection.

## Sensor Responsibilities

- **A3144 Hall sensor:** Primary wheel rotational speed source. Measure pulses with MCU-appropriate interrupt/timing mechanisms, calculate rotational speed, and convert it to vehicle speed using calibrated wheel circumference and pulses per revolution. Filtering and calibration must be configurable.
- **NEO-6M GPS:** Supplementary speed reference, latitude/longitude, timestamp, and geographic logging. Use it to cross-check Hall-derived speed. Do not automatically replace the Hall sensor as the primary speed source unless the architecture is explicitly changed and documented.
- **HC-SR04:** Forward obstacle/proximity measurement using a non-blocking measurement strategy, required filtering, and a verified safe electrical interface.
- **MPU6050:** Acceleration and angular-rate measurements for harsh braking, sudden acceleration, abnormal motion, and impact-related features. Calibration and filtering are required. It may provide input to accident detection and AI.

## Safety Architecture

This is a monitoring and alerting system. It must not directly control vehicle brakes, steering, throttle, the engine ECU, or safety-critical CAN functions. It warns/alerts the driver and reports events.

The deterministic safety engine should provide clear, testable rules for:

- Overspeed
- Unsafe proximity
- Combined speed and proximity risk
- Severe impact or accident indicators where implemented

Use configurable thresholds and hysteresis where appropriate. Never claim that a collision can be perfectly predicted.

## Alerts and Real-Time Behavior

Local alerts include a buzzer and LED. Alert levels must be clearly defined as deterministic states. Avoid blocking delays in the safety path; use non-blocking scheduling and state machines where appropriate.

## AI and Machine Learning

AI is an enhancement layer, not the primary safety authority. Potential responsibilities include driving-behavior classification, anomaly detection, sensor-fusion/risk scoring, event classification, and historical telemetry analysis.

Before training, define the dataset schema, preprocessing, feature engineering, training/inference separation, offline testing, measurable evaluation metrics, and model versioning. Keep models suitable for the UNO Q 2GB resource constraints. Never fabricate accuracy or claim successful inference until it has been tested.

## Cloud, Backend, and Dashboard

The project requires a cloud/backend endpoint for telemetry and monitoring. The eventual architecture should support vehicle telemetry, speed, obstacle distance, GPS position, alert level, IMU/event information, timestamps, connectivity status, important event history, and emergency events.

The dashboard should eventually visualize current/recorded speed, location, alerts, event history, telemetry trends, connectivity, and safety events.

Do not hard-code credentials. Use configuration/environment files and provide `.env.example` when appropriate. Never commit passwords, API keys, tokens, SIM credentials, Wi-Fi credentials, or private certificates.

## MCU-Linux Communication

Before implementing communication:

1. Identify the available UNO Q inter-domain communication mechanism.
2. Verify it using official documentation.
3. Document the message format and message IDs/types.
4. Document timestamps and sequence numbers where required.
5. Define error handling and timeout/recovery behavior.

Do not invent the UNO Q inter-domain transport. The MCU must continue basic safety operation when Linux is unavailable.

## Failure and Offline Behavior

Design for Wi-Fi loss, cloud unavailability, Linux service crashes, AI failure, LTE unavailability, sensor timeouts, invalid readings, GPS unavailability, corrupted/invalid messages, and MCU/Linux communication timeouts.

Communication failure must not disable local deterministic safety alerts. Where useful, buffer important events locally and upload them later.

## Testing and Validation

Every major subsystem should eventually have tests covering sensor input processing, filtering, speed calculation, proximity calculation, alert thresholds, hysteresis, accident/event detection, MCU/Linux communication, AI inference, backend APIs, cloud failure, offline recovery, the LTE emergency path, and end-to-end integration.

Separate simulated, bench-test, hardware-test, and field-test results. Never fabricate measurements. If a metric has not been measured, write:

`NOT YET MEASURED`

MATLAB/Simulink may be used for algorithm development, threshold analysis, filtering analysis, simulation, and verification of decision logic. Simulation is not physical validation; label all simulation results as simulation. Support every physical performance claim with actual measured test data.

## Phase-I Documents

Phase-I documents are reference material only. They may contain ESP32 architecture, old GPIO assignments, old software structure, theoretical/simulated claims, and historical decisions.

When Phase-I material conflicts with the current Phase-2 architecture, the current Phase-2 architecture wins. Preserve older algorithms or concepts only after checking compatibility with the UNO Q 2GB architecture. Do not copy old ESP32 pin mappings into UNO Q firmware or repeat historical performance claims as newly measured results.

## Code Quality

Use modular architecture, meaningful names, clear interfaces, comments for non-obvious engineering decisions, configuration separated from implementation, error handling, logging, unit tests where practical, reproducible builds, and version-controlled configuration.

Avoid giant monolithic files, unnecessary dependencies, blocking delays in real-time paths, hard-coded credentials, unexplained magic numbers, and duplicated logic.

## Development Process

Build incrementally in this order:

0. Architecture audit
1. Repository structure
2. MCU foundation
3. Sensor interfaces
4. Filtering and calibration
5. Deterministic safety engine
6. Buzzer/LED alert system
7. MCU/Linux communication
8. Linux service
9. Data logging
10. AI dataset pipeline
11. AI model development
12. Edge AI inference
13. Backend
14. Database
15. Dashboard
16. LTE emergency system
17. Offline/recovery handling
18. Full integration
19. Testing and validation
20. Documentation

At every stage:

1. Inspect the existing repository.
2. Identify dependencies.
3. Implement the smallest coherent unit.
4. Build and test it.
5. Fix errors.
6. Document important decisions.
7. Commit stable progress when directed by the user or project workflow.

Do not jump directly to documentation or claim completion of later stages without implementing and validating the required work.

## Repository Organization

Use this target structure unless inspection reveals a strong technical reason to change it:

```text
smart-speed-guard/
├── AGENTS.md
├── README.md
├── docs/
│   ├── architecture/
│   ├── hardware/
│   ├── protocol/
│   ├── testing/
│   └── phase1/
├── firmware/
│   ├── mcu/
│   └── linux/
├── ai/
├── backend/
├── dashboard/
├── simulation/
│   ├── matlab/
│   └── simulink/
├── tests/
├── scripts/
├── .env.example
└── .gitignore
```

Do not create directories merely for appearance. Create them when the relevant development stage begins.

## Academic Integrity

Do not fabricate experimental results, citations, hardware validation, field testing, or compliance with automotive safety standards. Clearly distinguish design, implementation, simulation, bench testing, field testing, measured results, and expected results.

## Unknown Information

If an important technical detail is unknown, do not guess. Identify the missing information, mark it `TODO: VERIFY`, explain what must be verified, and continue only if a safe assumption is possible.

Verification is mandatory for hardware interfaces, electrical limits, pin mappings, communication protocols, modem commands, and board-specific functionality.

## Scope Rule

For repository setup work, modify only the files explicitly requested. Do not generate application code, firmware, AI models, backend/dashboard code, fake implementation files, or random dependencies. Do not change hardware pin assignments, invent hardware specifications, or overwrite/delete existing files unless explicitly requested.

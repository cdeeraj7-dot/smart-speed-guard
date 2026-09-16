# Smart Speed Guard - AI Specification

## 1. Purpose

The AI module is a high-level decision-support component of the Smart Speed
Guard system.

It analyses vehicle telemetry and driving-behaviour data to identify patterns
associated with abnormal or risky driving.

The AI operates on the Linux/QRB2210 side of the Arduino UNO Q.

The AI does not directly control braking, steering, throttle, or other
vehicle-control systems.

The deterministic safety and alert functions remain independent of the AI.

---

## 2. AI Responsibilities

The AI module is responsible for:

- Receiving processed vehicle telemetry.
- Validating and preprocessing input data.
- Extracting relevant driving-behaviour features.
- Detecting abnormal driving patterns.
- Estimating a driving-risk score or risk state.
- Providing an interpretable AI output to the higher-level system.
- Logging inference inputs and outputs for evaluation.
- Handling invalid, missing, stale, or insufficient data safely.

The AI must not suppress or override deterministic safety alerts.

---

## 3. Candidate Input Data

The AI may use the following telemetry:

### Vehicle speed
- Wheel-speed measurement from the Hall-effect sensor.
- GPS-derived speed where available.
- Speed trend and changes over time.

### Vehicle dynamics
- MPU6050 accelerometer data.
- MPU6050 gyroscope data.
- Acceleration/deceleration patterns.
- Angular-motion patterns.

### Proximity
- HC-SR04 obstacle distance.
- Relationship between vehicle speed and obstacle distance.

### GPS
- Latitude.
- Longitude.
- GPS availability/fix status.

### System state
- Deterministic alert level.
- Sensor validity/status.
- Timestamp.
- Data freshness.

Only inputs that are actually available and verified during Phase 2
implementation will be enabled for the final AI model.

---

## 4. Candidate Features

Possible AI features include:

- Mean speed over a time window.
- Maximum speed over a time window.
- Speed variance.
- Speed change rate.
- Longitudinal acceleration statistics.
- Lateral acceleration statistics.
- Gyroscope statistics.
- Sudden braking events.
- Sudden acceleration events.
- Sudden lateral-motion events.
- Mean obstacle distance.
- Minimum obstacle distance.
- Rate of obstacle-distance change.
- Speed-to-distance relationship.
- Frequency of threshold violations.

Feature selection will be determined experimentally using collected data.

---

## 5. AI Output

The AI should produce a structured result containing, where supported:

- Risk score.
- Risk category.
- Detected behaviour/event.
- Confidence or model score.
- Timestamp.
- Input-data validity status.

Example conceptual output:

```json
{
	"risk_score": 0.0,
	"risk_level": "NORMAL",
	"event": "NONE",
	"confidence": 0.0,
	"timestamp": 0,
	"data_valid": true
}
```

The exact numerical scale and categories will be defined after model
selection and validation.

---

## 6. Safety Relationship

The AI is an enhancement layer.

The system must continue deterministic local safety monitoring if:

- The AI process stops.
- The Linux system restarts.
- Network connectivity is unavailable.
- Cloud services are unavailable.
- AI input data is invalid.
- AI inference fails.

An AI failure must never disable the primary MCU safety path.

---

## 7. Initial AI Approach

The first implementation should favour a lightweight model suitable for
edge execution on the Arduino UNO Q Linux/QRB2210 environment.

Candidate approaches:

- Statistical anomaly detection.
- Isolation Forest.
- One-Class classification.
- Lightweight supervised classification, if labelled data becomes available.

A final model will be selected only after data collection and feature
analysis.

Deep-learning models will not be assumed necessary.

---

## 8. Dataset Requirements

The dataset must contain timestamped sensor/telemetry samples.

Possible fields include:

- timestamp
- speed
- GPS speed
- latitude
- longitude
- acceleration_x
- acceleration_y
- acceleration_z
- gyroscope_x
- gyroscope_y
- gyroscope_z
- obstacle_distance
- deterministic_alert_level
- sensor_validity

The final dataset schema will be updated after the actual Phase 2 sensor
interfaces and sampling rates are verified.

No fabricated sensor measurements will be used as experimental results.

---

## 9. Development Pipeline

The AI development pipeline will follow:

Raw telemetry
	↓
Data validation
	↓
Preprocessing
	↓
Feature extraction
	↓
Dataset creation
	↓
Exploratory analysis
	↓
Model training
	↓
Model validation
	↓
Model export
	↓
Linux/QRB2210 inference
	↓
Risk output
	↓
Logging / cloud integration

---

## 10. Evaluation

The AI module will be evaluated using appropriate metrics based on the
selected learning approach.

Possible metrics include:

- Precision
- Recall
- F1-score
- Confusion matrix
- False-positive rate
- False-negative rate
- Inference latency
- CPU and memory usage

Metrics will only be reported after actual experiments have been performed.

---

## 11. Initial Feature Set

The first feature-extraction implementation will generate features from each
validated telemetry window.

### Speed features

- Mean Hall-effect speed.
- Maximum Hall-effect speed.
- Minimum Hall-effect speed.
- Speed standard deviation.
- Mean GPS speed when GPS data is valid.

### Acceleration features

- Mean acceleration magnitude.
- Maximum acceleration magnitude.
- Standard deviation of acceleration magnitude.

Acceleration magnitude is calculated as:

$$
\sqrt{accel_x^2 + accel_y^2 + accel_z^2}
$$

### Gyroscope features

- Mean gyroscope magnitude.
- Maximum gyroscope magnitude.
- Standard deviation of gyroscope magnitude.

Gyroscope magnitude is calculated as:

$$
\sqrt{gyro_x^2 + gyro_y^2 + gyro_z^2}
$$

### Obstacle-distance features

- Mean obstacle distance.
- Minimum obstacle distance.
- Standard deviation of obstacle distance.

### System-state features

- Number of deterministic alert observations.
- Percentage of records with valid sensor status.
- Percentage of records with valid GPS status.

### Feature-selection principle

The initial feature set is intentionally small and interpretable.

Features will be evaluated using actual Phase 2 telemetry before the final
machine-learning model is selected.

No experimentally derived thresholds are included in the feature extractor
at this stage.

---

## 12. Current Development Status

Phase 2 AI implementation has not yet been experimentally validated.

Current status:

- AI architecture: PLANNED
- Dataset: NOT YET COLLECTED
- Feature set: TO BE VERIFIED
- Model: NOT YET SELECTED
- Training: NOT STARTED
- Edge inference: NOT STARTED
- Performance metrics: NOT YET MEASURED

Phase 2 AI implementation has not yet been experimentally validated.

Current status:

- AI architecture: PLANNED
- Dataset: NOT YET COLLECTED
- Feature set: TO BE VERIFIED
- Model: NOT YET SELECTED
- Training: NOT STARTED
- Edge inference: NOT STARTED
- Performance metrics: NOT YET MEASURED

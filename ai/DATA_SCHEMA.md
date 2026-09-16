# Smart Speed Guard - AI Data Schema

## 1. Purpose

This document defines the initial telemetry format that will be used by the
Smart Speed Guard AI pipeline.

The schema is designed to support sensor-data collection, preprocessing,
feature extraction, model training, and Linux-side inference.

The schema is provisional and will be updated after the actual Phase 2
hardware interfaces and sampling rates are verified.

---

## 2. Raw Telemetry Record

Each record represents one timestamped observation.

| Field | Type | Unit | Description |
|---|---|---|---|
| timestamp | integer | ms | Timestamp of the observation |
| speed_hall | float | km/h | Speed derived from Hall-effect sensor |
| speed_gps | float | km/h | GPS-derived speed, when available |
| latitude | float | degrees | GPS latitude |
| longitude | float | degrees | GPS longitude |
| gps_valid | boolean | - | GPS validity/fix status |
| accel_x | float | m/s² | Accelerometer X-axis |
| accel_y | float | m/s² | Accelerometer Y-axis |
| accel_z | float | m/s² | Accelerometer Z-axis |
| gyro_x | float | deg/s | Gyroscope X-axis |
| gyro_y | float | deg/s | Gyroscope Y-axis |
| gyro_z | float | deg/s | Gyroscope Z-axis |
| obstacle_distance | float | cm | Distance measured by ultrasonic sensor |
| deterministic_alert | integer | - | MCU safety-alert state |
| sensor_valid | boolean | - | Overall sensor-data validity |

---

## 3. Data Validity

The AI pipeline must not silently treat invalid sensor values as valid data.

Possible invalid conditions include:

- Missing sensor measurement.
- Sensor timeout.
- GPS fix unavailable.
- Stale measurement.
- Out-of-range measurement.
- Corrupted telemetry record.
- Communication timeout.

Invalid fields must be explicitly represented.

---

## 4. Example Record

The following is only an example of the data format.

It is NOT an experimental measurement.

```json
{
	"timestamp": 0,
	"speed_hall": 0.0,
	"speed_gps": 0.0,
	"latitude": 0.0,
	"longitude": 0.0,
	"gps_valid": false,
	"accel_x": 0.0,
	"accel_y": 0.0,
	"accel_z": 0.0,
	"gyro_x": 0.0,
	"gyro_y": 0.0,
	"gyro_z": 0.0,
	"obstacle_distance": 0.0,
	"deterministic_alert": 0,
	"sensor_valid": false
}
```

---

## 6. Initial Windowing Configuration

The initial AI development pipeline will use:

- Window duration: 5 seconds.
- Window overlap: 50%.
- Timestamp unit: milliseconds.
- Minimum samples per window: configurable.
- Window boundaries will be determined from timestamps.

These values are initial development parameters and are not experimentally
validated.

The final window duration, overlap, and minimum sample count will be selected
after actual Phase 2 telemetry is collected and the sensor sampling behaviour
is verified.

import csv
import time
from pathlib import Path

from arduino.app_utils import App, Bridge


LOG_FILE = Path("telemetry.csv")
CSV_COLUMNS = (
    "mcu_timestamp_ms",
    "speed_hall",
    "speed_gps",
    "latitude",
    "longitude",
    "gps_valid",
    "accel_x",
    "accel_y",
    "accel_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "gyro_valid",
    "obstacle_distance",
    "deterministic_alert",
    "sensor_valid",
)


def initialize_log():
    if LOG_FILE.exists():
        with LOG_FILE.open("r", newline="") as file:
            existing_columns = next(csv.reader(file), None)

        if existing_columns != list(CSV_COLUMNS):
            raise ValueError(
                f"{LOG_FILE} has an incompatible telemetry schema"
            )
        return

    with LOG_FILE.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_COLUMNS)


def receive_telemetry(
    mcu_timestamp_ms,
    speed_hall,
    speed_gps,
    latitude,
    longitude,
    gps_valid,
    accel_x,
    accel_y,
    accel_z,
    gyro_x,
    gyro_y,
    gyro_z,
    gyro_valid,
    obstacle_distance,
    deterministic_alert,
    sensor_valid,
):
    with LOG_FILE.open("a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            mcu_timestamp_ms,
            speed_hall,
            speed_gps,
            latitude,
            longitude,
            gps_valid,
            accel_x,
            accel_y,
            accel_z,
            gyro_x,
            gyro_y,
            gyro_z,
            gyro_valid,
            obstacle_distance,
            deterministic_alert,
            sensor_valid,
        ])

    print(
        f"Telemetry logged | MCU time: {mcu_timestamp_ms} ms | "
        f"Speed: {speed_hall:.2f} | "
        f"Accel: ({accel_x:.3f}, {accel_y:.3f}, {accel_z:.3f}) g | "
        f"Alert: {deterministic_alert} | "
        f"Valid: {sensor_valid}"
    )


initialize_log()

Bridge.provide(
    "telemetry",
    receive_telemetry,
)


def loop():
    print("Linux telemetry logger running...")
    time.sleep(5)


App.run(user_loop=loop)
import csv
import time
from pathlib import Path

from arduino.app_utils import App, Bridge


LOG_FILE = Path("telemetry.csv")


def initialize_log():
    if not LOG_FILE.exists():
        with LOG_FILE.open("w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "timestamp_ms",
                "accel_x",
                "accel_y",
                "accel_z",
                "sensor_valid",
            ])


def receive_telemetry(
    accel_x,
    accel_y,
    accel_z,
    sensor_valid,
):
    timestamp_ms = int(time.time() * 1000)

    with LOG_FILE.open("a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp_ms,
            accel_x,
            accel_y,
            accel_z,
            sensor_valid,
        ])

    print(
        f"Telemetry logged | "
        f"X: {accel_x:.3f} g | "
        f"Y: {accel_y:.3f} g | "
        f"Z: {accel_z:.3f} g | "
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
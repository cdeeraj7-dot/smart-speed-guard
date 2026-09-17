from pathlib import Path
import sys

import pandas as pd
import streamlit as st


# -----------------------------
# Project path
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# AI pipeline imports
from ai.preprocessing.real_telemetry import (
    load_real_accelerometer_csv,
)
from ai.preprocessing.windowing import create_windows
from ai.features.extractor import (
    extract_available_sensor_features,
)


TELEMETRY_FILE = (
    PROJECT_ROOT
    / "ai"
    / "data"
    / "raw"
    / "real_telemetry.csv"
)


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Smart Speed Guard",
    page_icon="🚗",
    layout="wide",
)


# -----------------------------
# Title
# -----------------------------

st.title("Smart Speed Guard")

st.subheader(
    "Real-Time Automotive Safety and Speed Monitoring System"
)

st.markdown(
    "**Current telemetry source:** Real MPU6050 accelerometer "
    "data captured through the Arduino UNO Q."
)


# -----------------------------
# Load telemetry
# -----------------------------

if not TELEMETRY_FILE.exists():
    st.error(
        f"Telemetry file not found: {TELEMETRY_FILE}"
    )
    st.stop()


df = pd.read_csv(TELEMETRY_FILE)


# -----------------------------
# Validate telemetry
# -----------------------------

required_columns = {
    "timestamp_ms",
    "accel_x",
    "accel_y",
    "accel_z",
    "sensor_valid",
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(
        f"Missing telemetry columns: {sorted(missing_columns)}"
    )
    st.stop()


if df.empty:
    st.error("Telemetry file contains no records.")
    st.stop()


# -----------------------------
# Prepare telemetry
# -----------------------------

df["accel_magnitude"] = (
    df["accel_x"] ** 2
    + df["accel_y"] ** 2
    + df["accel_z"] ** 2
) ** 0.5


df["elapsed_seconds"] = (
    df["timestamp_ms"] - df["timestamp_ms"].iloc[0]
) / 1000.0


# -----------------------------
# AI preprocessing
# -----------------------------

records = load_real_accelerometer_csv(
    TELEMETRY_FILE
)

windows = create_windows(
    records,
    window_ms=5000,
    overlap=0.5,
    min_samples=1,
)

if not windows:
    st.error("No telemetry windows could be created.")
    st.stop()


ai_features = extract_available_sensor_features(
    windows[0]
)


# -----------------------------
# System status
# -----------------------------

st.header("System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Telemetry Samples",
        len(df),
    )

with col2:
    valid_percentage = (
        df["sensor_valid"].mean() * 100
    )

    st.metric(
        "Sensor Validity",
        f"{valid_percentage:.1f}%",
    )

with col3:
    st.metric(
        "Maximum Acceleration",
        f"{df['accel_magnitude'].max():.2f} g",
    )


st.divider()


# -----------------------------
# AI features
# -----------------------------

st.header("AI Sensor Features")

st.caption(
    "Features extracted from the first 5-second telemetry "
    "window using the project's sensor-aware preprocessing "
    "pipeline."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Mean Acceleration",
        f"{ai_features['accel_magnitude_mean']:.4f} g",
    )

with col2:
    st.metric(
        "Maximum Acceleration",
        f"{ai_features['accel_magnitude_max']:.4f} g",
    )

with col3:
    st.metric(
        "Acceleration Std. Dev.",
        f"{ai_features['accel_magnitude_std']:.4f} g",
    )

with col4:
    st.metric(
        "Sensor Validity",
        f"{ai_features['sensor_valid_percentage'] * 100:.1f}%",
    )


st.info(
    "Currently available AI input: MPU6050 accelerometer. "
    "GPS, Hall-effect, gyroscope and ultrasonic features "
    "are not yet included because those sensors are not "
    "currently providing verified telemetry."
)


st.divider()


# -----------------------------
# Accelerometer telemetry
# -----------------------------

st.header("Accelerometer Telemetry")

acceleration_chart = df.set_index(
    "elapsed_seconds"
)[
    [
        "accel_x",
        "accel_y",
        "accel_z",
    ]
]

st.line_chart(acceleration_chart)


# -----------------------------
# Acceleration magnitude
# -----------------------------

st.header("Acceleration Magnitude")

magnitude_chart = df.set_index(
    "elapsed_seconds"
)[
    [
        "accel_magnitude",
    ]
]

st.line_chart(magnitude_chart)


st.divider()


# -----------------------------
# Raw telemetry
# -----------------------------

st.header("Raw Telemetry")

st.dataframe(
    df[
        [
            "timestamp_ms",
            "accel_x",
            "accel_y",
            "accel_z",
            "accel_magnitude",
            "sensor_valid",
        ]
    ],
    use_container_width=True,
)


# -----------------------------
# Architecture note
# -----------------------------

st.caption(
    "This dashboard is a monitoring and visualization layer. "
    "It is not part of the deterministic MCU safety path."
)

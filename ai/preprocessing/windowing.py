from __future__ import annotations

from typing import Any


def create_windows(
	records: list[dict[str, Any]],
	window_ms: int = 5000,
	overlap: float = 0.5,
	min_samples: int = 1,
) -> list[list[dict[str, Any]]]:
	"""
	Group timestamped telemetry records into overlapping time windows.

	Args:
		records: Timestamped telemetry records.
		window_ms: Window duration in milliseconds.
		overlap: Fraction of overlap between consecutive windows.
		min_samples: Minimum number of records required in a window.

	Returns:
		A list containing telemetry windows.

	Raises:
		ValueError: If window parameters are invalid.
	"""

	if window_ms <= 0:
		raise ValueError("window_ms must be greater than zero")

	if not 0 <= overlap < 1:
		raise ValueError("overlap must be between 0 and 1")

	if min_samples <= 0:
		raise ValueError("min_samples must be greater than zero")

	if not records:
		return []

	# Work on a timestamp-ordered copy.
	sorted_records = sorted(records, key=lambda record: record["timestamp"])

	step_ms = window_ms * (1 - overlap)

	windows: list[list[dict[str, Any]]] = []

	start_time = sorted_records[0]["timestamp"]
	end_time = sorted_records[-1]["timestamp"]

	current_start = start_time

	while current_start <= end_time:
		current_end = current_start + window_ms

		window = [
			record
			for record in sorted_records
			if current_start <= record["timestamp"] < current_end
		]

		if len(window) >= min_samples:
			windows.append(window)

		current_start += step_ms

	return windows

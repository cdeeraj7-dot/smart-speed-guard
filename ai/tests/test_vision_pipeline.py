import pytest

from ai.vision.pipeline import VisionEventPipeline


def make_record(timestamp, alert, alert_type=None):
    record = {
        "timestamp": timestamp,
        "deterministic_alert": alert,
    }
    if alert_type is not None:
        record["alert_type"] = alert_type
    return record


def test_builds_event_context_when_trigger_requests_capture():
    pipeline = VisionEventPipeline()

    result = pipeline.process(
        make_record(1_000, 1, "unsafe proximity"),
        detections=[
            {"class_name": "car", "confidence": 0.9},
            {"class_name": "person", "confidence": 0.4},
        ],
    )

    assert result == {
        "capture_requested": True,
        "event_context": {
            "event_id": 1,
            "timestamp": 1_000,
            "alert_type": "UNSAFE PROXIMITY",
            "visual_context": {
                "person": 0,
                "car": 1,
                "motorcycle": 0,
                "bicycle": 0,
                "bus": 0,
                "truck": 0,
                "other": 0,
            },
            "detections": [{"class_name": "car", "confidence": 0.9}],
            "detection_count": 1,
        },
    }


def test_non_triggering_record_has_no_event_context():
    pipeline = VisionEventPipeline()

    assert pipeline.process(make_record(0, 0)) == {
        "capture_requested": False,
        "event_context": None,
    }


def test_repeated_alert_does_not_create_another_context():
    pipeline = VisionEventPipeline()

    pipeline.process(make_record(1_000, 1))
    result = pipeline.process(make_record(1_500, 1))

    assert result == {
        "capture_requested": False,
        "event_context": None,
    }


def test_new_contexts_receive_incrementing_event_ids():
    pipeline = VisionEventPipeline(cooldown_ms=1_000)

    first = pipeline.process(make_record(0, 1))
    pipeline.process(make_record(100, 0))
    second = pipeline.process(make_record(1_000, 2))

    assert first["event_context"]["event_id"] == 1
    assert second["event_context"]["event_id"] == 2


def test_missing_detections_and_alert_type_use_defaults():
    pipeline = VisionEventPipeline()

    result = pipeline.process(make_record(100, 1))

    assert result["event_context"]["alert_type"] == "UNKNOWN"
    assert result["event_context"]["detections"] == []
    assert result["event_context"]["detection_count"] == 0


def test_invalid_context_data_is_reported():
    pipeline = VisionEventPipeline()

    with pytest.raises(ValueError, match="Each detection must be a dictionary"):
        pipeline.process(make_record(100, 1), detections=[None])

def test_processes_arduino_output_through_vision_pipeline():
    pipeline = VisionEventPipeline()

    arduino_output = {
        "detection": [
            {
                "class_name": "car",
                "confidence": 69.65,
                "bounding_box_xyxy": [61.73, 71.42, 88.48, 94.06],
            },
            {
                "class_name": "motorcycle",
                "confidence": 55.25,
                "bounding_box_xyxy": [36.52, 88.91, 81.79, 121.32],
            },
            {
                "class_name": "person",
                "confidence": 46.46,
                "bounding_box_xyxy": [51.95, 78.62, 67.38, 109.49],
            },
        ]
    }

    result = pipeline.process_arduino_output(
        record=make_record(1000, 1, "unsafe proximity"),
        arduino_output=arduino_output,
    )

    context = result["event_context"]

    assert result["capture_requested"] is True
    assert context["event_id"] == 1
    assert context["alert_type"] == "UNSAFE PROXIMITY"

    # Person detection is filtered below the 50% threshold.
    assert context["detection_count"] == 2
    assert context["visual_context"]["car"] == 1
    assert context["visual_context"]["motorcycle"] == 1
    assert context["visual_context"]["person"] == 0

    # Confidence is converted from percentage to fraction.
    assert context["detections"][0]["confidence"] == pytest.approx(0.6965)
    assert context["detections"][1]["confidence"] == pytest.approx(0.5525)

    # Original bounding boxes are preserved.
    assert context["detections"][0]["bounding_box_xyxy"] == [
        61.73, 71.42, 88.48, 94.06
    ]


def test_arduino_output_without_safety_trigger_creates_no_context():
    pipeline = VisionEventPipeline()

    result = pipeline.process_arduino_output(
        record=make_record(1000, 0),
        arduino_output={"detection": []},
    )

    assert result == {
        "capture_requested": False,
        "event_context": None,
    }

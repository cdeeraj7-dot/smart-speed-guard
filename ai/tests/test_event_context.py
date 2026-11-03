import pytest

from ai.vision.arduino_adapter import adapt_arduino_detections
from ai.vision.event_context import SUPPORTED_OBJECTS, create_event_context


def test_creates_context_with_normalized_detection_classes():
    result = create_event_context(
        event_id=12,
        timestamp=34_000,
        alert_type=" unsafe proximity ",
        detections=[
            {"class_name": "Car", "confidence": 0.9},
            {"class_name": "pedestrian", "confidence": 0.75},
            {"class_name": "truck", "confidence": 0.49},
        ],
    )

    assert result == {
        "event_id": 12,
        "timestamp": 34_000,
        "alert_type": "UNSAFE PROXIMITY",
        "visual_context": {
            name: int(name in {"car", "other"})
            for name in SUPPORTED_OBJECTS
        },
        "detections": [
            {"class_name": "car", "confidence": 0.9},
            {"class_name": "other", "confidence": 0.75},
        ],
        "detection_count": 2,
    }


def test_empty_detections_returns_zero_counts():
    result = create_event_context(0, 0, "overspeed", [])

    assert result["detection_count"] == 0
    assert result["detections"] == []
    assert all(count == 0 for count in result["visual_context"].values())


def test_confidence_threshold_is_inclusive():
    result = create_event_context(
        1,
        100,
        "overspeed",
        [{"class_name": "person", "confidence": 0.7}],
        min_confidence=0.7,
    )

    assert result["detection_count"] == 1
    assert result["visual_context"]["person"] == 1


@pytest.mark.parametrize(
    ("args", "message"),
    [
        ((-1, 0, "overspeed", []), "event_id must be a non-negative integer"),
        ((True, 0, "overspeed", []), "event_id must be a non-negative integer"),
        ((1, -1, "overspeed", []), "timestamp must be a non-negative integer"),
        ((1, True, "overspeed", []), "timestamp must be a non-negative integer"),
        ((1, 0, "", []), "alert_type must be a non-empty string"),
        ((1, 0, "overspeed", ()), "detections must be a list"),
    ],
)
def test_rejects_invalid_event_fields(args, message):
    with pytest.raises(ValueError, match=message):
        create_event_context(*args)


@pytest.mark.parametrize(
    "threshold",
    [
        -0.1,
        1.1,
    ],
)
def test_rejects_out_of_range_minimum_confidence(threshold):
    with pytest.raises(ValueError, match="min_confidence must be between 0 and 1"):
        create_event_context(
            1,
            0,
            "overspeed",
            [{"class_name": "car", "confidence": 0.5}],
            min_confidence=threshold,
        )


def test_rejects_non_numeric_minimum_confidence():
    with pytest.raises(ValueError, match="min_confidence must be numeric"):
        create_event_context(1, 0, "overspeed", [], min_confidence=True)


@pytest.mark.parametrize(
    ("detection", "message"),
    [
        (None, "Each detection must be a dictionary"),
        ({"class_name": "car"}, "Detection requires class_name and confidence"),
        (
            {"class_name": "", "confidence": 0.8},
            "class_name must be a non-empty string",
        ),
        (
            {"class_name": "car", "confidence": False},
            "confidence must be numeric",
        ),
        (
            {"class_name": "car", "confidence": 1.1},
            "confidence must be between 0 and 1",
        ),
    ],
)
def test_rejects_invalid_detections(detection, message):
    with pytest.raises(ValueError, match=message):
        create_event_context(1, 0, "overspeed", [detection])

def test_preserves_bounding_box_in_event_context():
    result = create_event_context(
        event_id=1,
        timestamp=1000,
        alert_type="overspeed",
        detections=[
            {
                "class_name": "car",
                "confidence": 0.85,
                "bounding_box_xyxy": [10, 20, 80, 100],
            }
        ],
    )

    assert result["detections"][0] == {
        "class_name": "car",
        "confidence": 0.85,
        "bounding_box_xyxy": [10.0, 20.0, 80.0, 100.0],
    }


def test_supports_detections_without_bounding_boxes():
    result = create_event_context(
        1,
        1000,
        "overspeed",
        [{"class_name": "person", "confidence": 0.9}],
    )

    assert result["detections"] == [
        {"class_name": "person", "confidence": 0.9}
    ]


@pytest.mark.parametrize(
    "bounding_box",
    [
        [0, 1, 2],
        [0, 1, 2, float("nan")],
        [0, 1, 2, True],
        [10, 20, 5, 30],
        [10, 30, 20, 25],
    ],
)
def test_rejects_invalid_bounding_boxes(bounding_box):
    with pytest.raises(ValueError):
        create_event_context(
            1,
            1000,
            "overspeed",
            [
                {
                    "class_name": "car",
                    "confidence": 0.9,
                    "bounding_box_xyxy": bounding_box,
                }
            ],
        )


def test_integrates_arduino_detections_with_event_context():
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

    adapted_detections = adapt_arduino_detections(arduino_output)

    result = create_event_context(
        event_id=1,
        timestamp=1000,
        alert_type="unsafe_proximity",
        detections=adapted_detections,
    )

    assert result["detection_count"] == 2
    assert result["visual_context"]["car"] == 1
    assert result["visual_context"]["motorcycle"] == 1
    assert result["visual_context"]["person"] == 0

    assert result["detections"][0]["confidence"] == pytest.approx(0.6965)
    assert result["detections"][1]["confidence"] == pytest.approx(0.5525)

    assert "bounding_box_xyxy" in result["detections"][0]
    assert "bounding_box_xyxy" in result["detections"][1]

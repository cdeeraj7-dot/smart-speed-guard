import pytest

from ai.vision.arduino_adapter import adapt_arduino_detections


def make_detection(class_name=" Car ", confidence=85, bounding_box=(1, 2, 30, 40)):
    return {
        "class_name": class_name,
        "confidence": confidence,
        "bounding_box_xyxy": bounding_box,
    }


def test_adapts_confidence_and_preserves_xyxy_box():
    result = adapt_arduino_detections(
        {"detection": [make_detection()]}
    )

    assert result == [
        {
            "class_name": "car",
            "confidence": 0.85,
            "bounding_box_xyxy": [1.0, 2.0, 30.0, 40.0],
        }
    ]


def test_missing_detection_field_returns_empty_list():
    assert adapt_arduino_detections({}) == []


@pytest.mark.parametrize("confidence", [0, 100])
def test_accepts_confidence_boundaries(confidence):
    result = adapt_arduino_detections(
        {"detection": [make_detection(confidence=confidence)]}
    )

    assert result[0]["confidence"] == confidence / 100


@pytest.mark.parametrize(
    ("output", "message"),
    [
        ([], "Detection output must be a dictionary"),
        ({"detection": {}}, "'detection' must be a list"),
        ({"detection": [None]}, "Detection 0 must be a dictionary"),
        (
            {"detection": [{"confidence": 50, "bounding_box_xyxy": [0, 0, 1, 1]}]},
            "Detection 0 has an invalid class_name",
        ),
        (
            {"detection": [make_detection(class_name=" ")]},
            "Detection 0 has an invalid class_name",
        ),
        (
            {"detection": [make_detection(confidence=True)]},
            "Detection 0 has invalid confidence",
        ),
        (
            {"detection": [make_detection(confidence=float("nan"))]},
            "Detection 0 has invalid confidence",
        ),
        (
            {"detection": [make_detection(confidence=float("inf"))]},
            "Detection 0 has invalid confidence",
        ),
        (
            {"detection": [make_detection(confidence=-1)]},
            "Detection 0 has invalid confidence",
        ),
        (
            {"detection": [make_detection(confidence=101)]},
            "Detection 0 has invalid confidence",
        ),
        (
            {"detection": [make_detection(bounding_box=[0, 1, 2])]},
            "Detection 0 has an invalid bounding box",
        ),
        (
            {"detection": [make_detection(bounding_box=[0, 1, 2, float("nan")])]},
            "Detection 0 has non-numeric bounding box coordinates",
        ),
        (
            {"detection": [make_detection(bounding_box=[0, 1, 2, True])]},
            "Detection 0 has non-numeric bounding box coordinates",
        ),
    ],
)
def test_rejects_invalid_detection_output(output, message):
    with pytest.raises(ValueError, match=message):
        adapt_arduino_detections(output)

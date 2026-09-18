import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from evidence_gate import evaluate


def base():
    return {
        "prediction_error": 1.0,
        "null_error": 2.0,
        "controls_pass": True,
        "falsification_attempted": True,
        "uncertainty_reported": True,
    }


def test_wrong_numeric_type_is_invalid():
    assert evaluate({**base(), "prediction_error": "1"}) == "INVALID"


def test_negative_error_is_invalid():
    assert evaluate({**base(), "null_error": -1}) == "INVALID"


def test_wrong_boolean_type_is_invalid():
    assert evaluate({**base(), "controls_pass": 1}) == "INVALID"

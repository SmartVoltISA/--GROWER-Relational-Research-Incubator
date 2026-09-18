import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from boundary_gate import evaluate as evaluate_boundary
from grower_core import GrowthCycle, Hypothesis, Relation, Status


def cycle():
    c = GrowthCycle("C-1", "test", [Relation("A", "r", "B")])
    c.add_hypothesis(Hypothesis("H1", "A affects B", "A does not affect B"))
    c.add_hypothesis(Hypothesis("H2", "B affects A", "B does not affect A"))
    c.lock_for_testing()
    return c


def test_supported_requires_evaluated_evidence_and_boundary():
    c = cycle()
    try:
        c.decide(Status.SUPPORTED, "claimed")
    except PermissionError:
        pass
    else:
        raise AssertionError("unsupported result was promoted")
    record = {
        "prediction_error": 1.0, "null_error": 2.0,
        "controls_pass": True, "falsification_attempted": True,
        "uncertainty_reported": True,
        "evidence_id": "E-SUPPORTED",
    }
    assert c.record_test_result(record, boundary_status=evaluate_boundary({"falsification_attempted": True, "controls_pass": True, "uncertainty_reported": True})) == "SUPPORTED"
    c.decide(Status.SUPPORTED, "evaluated evidence and boundary passed")
    assert c.status is Status.SUPPORTED


def test_weak_evidence_cannot_be_promoted():
    c = cycle()
    record = {
        "prediction_error": 1.0, "null_error": 2.0,
        "controls_pass": True, "falsification_attempted": False,
        "uncertainty_reported": True,
    }
    assert c.record_test_result(record, boundary_status="ADMISSIBLE") == "NOT_PROVEN"
    try:
        c.decide(Status.SUPPORTED, "claimed")
    except PermissionError:
        pass
    else:
        raise AssertionError("weak evidence was promoted")

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from assembler import issue_certificate
from grower_core import GrowthCycle, Hypothesis, Relation, Status
from boundary_gate import evaluate

def make_cycle():
    c = GrowthCycle("INPUT-FP", "test", [Relation("A", "r", "B")])
    c.add_hypothesis(Hypothesis("H1", "A", "not A"))
    c.add_hypothesis(Hypothesis("H2", "B", "not B"))
    c.lock_for_testing()
    c.record_test_result({
        "prediction_error": 1.0, "null_error": 2.0,
        "controls_pass": True, "falsification_attempted": True,
        "uncertainty_reported": True, "evidence_id": "E1",
    }, boundary_status=evaluate({
        "falsification_attempted": True, "controls_pass": True,
        "uncertainty_reported": True,
    }))
    c.decide(Status.SUPPORTED, "gated")
    return c

def test_certificate_binds_verified_cycle_inputs():
    c = make_cycle()
    cert = issue_certificate(c, "E1")
    assert cert.input_fingerprint == c._locked_fingerprint

def test_certificate_cannot_be_issued_after_supported_cycle_input_mutation():
    c = make_cycle()
    c.hypotheses[0].claim = "mutated after support"
    try:
        issue_certificate(c, "E1")
    except PermissionError:
        pass
    else:
        raise AssertionError("certificate issued for mutated supported cycle")

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from grower_core import Status
from growth_engine import Branch, select_next, should_stop
from assembler import Component, assemble, issue_certificate


def test_selects_active_testing_branch():
    a = Branch("A", Status.CANDIDATE)
    b = Branch("B", Status.TESTING, evidence_count=2)
    assert select_next([a, b]).branch_id == "B"


def test_stop_requires_falsification_controls_uncertainty():
    b = Branch("B", Status.TESTING, falsification_attempted=False, controls_passed=True, uncertainty_reported=True)
    assert should_stop(b)[0] is False
    b = Branch("B", Status.TESTING, falsification_attempted=True, controls_passed=True, uncertainty_reported=True)
    assert should_stop(b)[0] is True


def test_assembler_rejects_unverified_components():
    try:
        assemble([Component("C1", Status.PARTIAL, ("E1",), "math")], "target")
    except ValueError:
        pass
    else:
        raise AssertionError("unverified component was assembled")


def test_assembler_accepts_supported_components():
    from grower_core import GrowthCycle, Hypothesis, Relation
    cycle = GrowthCycle("CERT-1", "test", [Relation("A", "r", "B")])
    cycle.add_hypothesis(Hypothesis("H1", "A", "not A"))
    cycle.add_hypothesis(Hypothesis("H2", "B", "not B"))
    cycle.lock_for_testing()
    cycle.record_test_result({
        "prediction_error": 1.0, "null_error": 2.0,
        "controls_pass": True, "falsification_attempted": True,
        "uncertainty_reported": True, "evidence_id": "E1",
    }, boundary_status="ADMISSIBLE")
    cycle.decide(Status.SUPPORTED, "gated evidence")
    cert = issue_certificate(cycle, "E1")
    result = assemble([Component("C1", Status.SUPPORTED, ("E1",), "math", ("A",), cert)], "target")
    assert result["status"] == "ASSEMBLED"
    assert result["promotion"] == "EXTERNAL_HUMAN_DECISION_REQUIRED"
    assert result["promotion"] == "EXTERNAL_HUMAN_DECISION_REQUIRED"

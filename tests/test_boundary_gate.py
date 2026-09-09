import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from boundary_gate import evaluate


def valid():
    return {
        "falsification_attempted": True,
        "controls_pass": True,
        "uncertainty_reported": True,
    }


def test_valid_candidate_is_admissible():
    assert evaluate(valid()).status == "ADMISSIBLE"


def test_invariant_violation_is_hard_fail():
    c = {**valid(), "invariant_violations": ["guardian_authority"]}
    assert evaluate(c).status == "FAIL"


def test_boundary_change_requires_human_gate():
    c = {**valid(), "boundary_change_proposed": True}
    assert evaluate(c).status == "BOUNDARY_REVIEW_REQUIRED"
    assert evaluate(c, human_boundary_approval=True).status == "ADMISSIBLE"


def test_canonical_space_mutation_is_rejected():
    c = {**valid(), "canonical_space_mutated": True}
    assert evaluate(c).status == "FAIL"


def test_missing_falsification_is_not_proven():
    c = {"controls_pass": True, "uncertainty_reported": True}
    assert evaluate(c).status == "NOT_PROVEN"

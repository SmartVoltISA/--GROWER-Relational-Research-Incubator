import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from grower_core import Hypothesis, Relation, Status
from grow_cycle import attach_observation, propose_test_plan, seed_cycle
from evidence_gate import evaluate


def test_cycle_requires_competing_hypotheses():
    relations = [Relation("A", "connected_to", "B")]
    hs = [Hypothesis("H1", "A affects B", "A does not affect B"), Hypothesis("H2", "B affects A", "B does not affect A")]
    cycle = seed_cycle("T-001", "find directional relation", relations, hs)
    assert cycle.status == Status.TESTING
    assert len(propose_test_plan(cycle)) == 4


def test_observation_requires_uncertainty():
    relations = [Relation("A", "r", "B")]
    hs = [Hypothesis("H1", "claim 1", "null 1"), Hypothesis("H2", "claim 2", "null 2")]
    cycle = seed_cycle("T-002", "test", relations, hs)
    attach_observation(cycle, {"id": "obs-1", "protocol": "P1", "result": 1.2, "uncertainty": 0.1})
    assert len(cycle.evidence) == 1


def test_gate_is_conservative():
    good = {"prediction_error": 1.0, "null_error": 2.0, "controls_pass": True, "falsification_attempted": True, "uncertainty_reported": True}
    weak = {**good, "falsification_attempted": False}
    assert evaluate(good) == "SUPPORTED"
    assert evaluate(weak) == "NOT_PROVEN"

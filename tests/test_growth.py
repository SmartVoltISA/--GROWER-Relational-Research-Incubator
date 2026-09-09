import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from grower_core import Relation
from hypothesis_grower import grow_hypotheses
from branch_archive import BranchRecord, archive_branch, serialize


def test_growth_creates_competing_directions():
    cs = grow_hypotheses([Relation("A", "r", "B")])
    assert len(cs) == 2
    assert cs[0].hypothesis.id != cs[1].hypothesis.id
    assert cs[0].hypothesis.null_hypothesis
    assert cs[1].hypothesis.null_hypothesis


def test_archive_preserves_failed_branch():
    archive = []
    record = BranchRecord("B-1", None, "FAIL", "counterexample", ("E-1",))
    archive_branch(record, archive)
    assert archive[0]["status"] == "FAIL"
    assert "counterexample" in serialize(record)

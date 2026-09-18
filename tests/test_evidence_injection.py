import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from grower_core import GrowthCycle, Hypothesis, Relation

def test_direct_test_result_injection_is_blocked():
    c=GrowthCycle("C","test",[Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A"))
    c.add_hypothesis(Hypothesis("H2","B","not B"))
    c.lock_for_testing()
    try:
        c.record_evidence({"type":"test_result","evidence_status":"SUPPORTED","boundary_status":"ADMISSIBLE"})
    except PermissionError:
        pass
    else:
        raise AssertionError("direct test-result injection was accepted")

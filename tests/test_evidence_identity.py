import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from grower_core import GrowthCycle,Hypothesis,Relation
from boundary_gate import evaluate

def test_duplicate_test_evidence_id_is_rejected():
    c=GrowthCycle("EID-1","test",[Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A")); c.add_hypothesis(Hypothesis("H2","B","not B")); c.lock_for_testing()
    r={"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True,"evidence_id":"E1"}
    gate=evaluate({"falsification_attempted":True,"controls_pass":True,"uncertainty_reported":True})
    c.record_test_result(r,boundary_status=gate)
    try: c.record_test_result(r,boundary_status=gate)
    except ValueError: pass
    else: raise AssertionError("duplicate evidence ID accepted")

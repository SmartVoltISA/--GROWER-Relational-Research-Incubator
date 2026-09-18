import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from grower_core import GrowthCycle, Hypothesis, Relation, Status
from boundary_gate import evaluate

def test_mutated_evidence_cannot_be_promoted():
    c=GrowthCycle("TAMPER-1","test",[Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A"))
    c.add_hypothesis(Hypothesis("H2","B","not B"))
    c.lock_for_testing()
    record={"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True,"evidence_id":"E1"}
    c.record_test_result(record,boundary_status=evaluate({"falsification_attempted":True,"controls_pass":True,"uncertainty_reported":True}))
    c.evidence[0]["prediction_error"]=999.0
    c.evidence[0]["null_error"]=0.1
    try:
        c.decide(Status.SUPPORTED,"tampered")
    except PermissionError:
        pass
    else:
        raise AssertionError("mutated evidence was accepted")

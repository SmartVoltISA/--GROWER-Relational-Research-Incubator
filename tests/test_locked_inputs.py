import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from grower_core import GrowthCycle,Hypothesis,Relation,Status
from boundary_gate import evaluate

def test_mutated_hypothesis_after_lock_blocks_support():
    c=GrowthCycle("LOCK-1","test",[Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A"))
    c.add_hypothesis(Hypothesis("H2","B","not B"))
    c.lock_for_testing()
    c.hypotheses[0].claim="tampered"
    record={"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True,"evidence_id":"E1"}
    c.record_test_result(record,boundary_status=evaluate({"falsification_attempted":True,"controls_pass":True,"uncertainty_reported":True}))
    try:
        c.decide(Status.SUPPORTED,"tampered inputs")
    except PermissionError:
        pass
    else:
        raise AssertionError("mutated locked inputs were accepted")

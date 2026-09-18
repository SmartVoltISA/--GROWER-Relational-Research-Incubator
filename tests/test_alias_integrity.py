import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from grower_core import GrowthCycle,Hypothesis,Relation,Status
from boundary_gate import evaluate

def _cycle(relations,hypotheses):
    c=GrowthCycle("ALIAS-1","test",relations)
    for h in hypotheses: c.add_hypothesis(h)
    c.lock_for_testing()
    return c

def test_external_hypothesis_mutation_is_detected():
    h1=Hypothesis("H1","A","not A")
    h2=Hypothesis("H2","B","not B")
    c=_cycle([Relation("A","r","B")],[h1,h2])
    h1.claim="changed through external alias"
    rec={"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True,"evidence_id":"E1"}
    c.record_test_result(rec,boundary_status=evaluate({"falsification_attempted":True,"controls_pass":True,"uncertainty_reported":True}))
    try: c.decide(Status.SUPPORTED,"alias attack")
    except PermissionError: pass
    else: raise AssertionError("external hypothesis alias was accepted")

def test_relation_nested_value_alias_is_detected():
    nested={"weight":1}
    rel=Relation("A","r","B",value=nested)
    c=_cycle([rel],[Hypothesis("H1","A","not A"),Hypothesis("H2","B","not B")])
    nested["weight"]=999
    rec={"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True,"evidence_id":"E2"}
    c.record_test_result(rec,boundary_status=evaluate({"falsification_attempted":True,"controls_pass":True,"uncertainty_reported":True}))
    try: c.decide(Status.SUPPORTED,"nested alias attack")
    except PermissionError: pass
    else: raise AssertionError("nested relation alias was accepted")

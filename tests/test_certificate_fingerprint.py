import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from assembler import Component, VerificationCertificate, assemble, issue_certificate
from grower_core import GrowthCycle,Hypothesis,Relation,Status
from boundary_gate import evaluate

def make_cycle():
    c=GrowthCycle("CERT-FP","test",[Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A")); c.add_hypothesis(Hypothesis("H2","B","not B")); c.lock_for_testing()
    c.record_test_result({"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True,"evidence_id":"E1"},boundary_status=evaluate({"falsification_attempted":True,"controls_pass":True,"uncertainty_reported":True}))
    c.decide(Status.SUPPORTED,"gated")
    return c

def test_certificate_carries_evidence_fingerprint():
    c=make_cycle(); cert=issue_certificate(c,"E1")
    assert cert.evidence_fingerprint
    assert cert.cycle_id=="CERT-FP"

def test_forged_certificate_missing_fingerprint_is_blocked():
    c=make_cycle()
    from assembler import _CERTIFICATE_ISSUER
    cert=VerificationCertificate("CERT-FP","E1","","",_CERTIFICATE_ISSUER)
    try: assemble([Component("C",Status.SUPPORTED,("E1",),"x",certificate=cert,cycle_id="CERT-FP")],"T")
    except PermissionError: pass
    else: raise AssertionError("certificate without evidence fingerprint was accepted")

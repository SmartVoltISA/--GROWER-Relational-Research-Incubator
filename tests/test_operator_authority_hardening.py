import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from operator_authority import OperatorAuthority,SurgeryRequest,ProtectedTarget

def req(**kw):
    base={"change_id":"C1","target":ProtectedTarget.GROWTH_BOUNDARY,"operator_id":"OP1","request_id":"R1","confirmed":True}
    base.update(kw); return SurgeryRequest(**base)

def test_empty_proof_rejected():
    a=OperatorAuthority(lambda p,r: True)
    try: a.authorize(req(),"")
    except PermissionError: pass
    else: raise AssertionError("empty proof accepted")

def test_verifier_must_return_true():
    for result in (1,"true",object()):
        a=OperatorAuthority(lambda p,r,result=result: result)
        try: a.authorize(req(),"proof")
        except PermissionError: pass
        else: raise AssertionError("non-bool verifier result accepted")

def test_verifier_exception_is_fail_closed():
    def bad(p,r): raise RuntimeError("backend down")
    a=OperatorAuthority(bad)
    try: a.authorize(req(),"proof")
    except PermissionError: pass
    else: raise AssertionError("verifier exception opened authority")

def test_empty_identity_fields_rejected():
    a=OperatorAuthority(lambda p,r: True)
    for kw in ({"change_id":""},{"operator_id":""},{"request_id":""}):
        try: a.authorize(req(**kw),"proof")
        except ValueError: pass
        else: raise AssertionError("empty authority binding accepted")

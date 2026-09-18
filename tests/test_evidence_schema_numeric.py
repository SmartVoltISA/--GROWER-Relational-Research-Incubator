import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from evidence_gate import evaluate

BASE={"prediction_error":1.0,"null_error":2.0,"controls_pass":True,"falsification_attempted":True,"uncertainty_reported":True}

def test_bool_is_not_numeric():
    assert evaluate({**BASE,"prediction_error":True})=="INVALID"
    assert evaluate({**BASE,"null_error":False})=="INVALID"

def test_non_finite_float_is_invalid():
    assert evaluate({**BASE,"prediction_error":float("nan")})=="INVALID"
    assert evaluate({**BASE,"null_error":float("inf")})=="INVALID"

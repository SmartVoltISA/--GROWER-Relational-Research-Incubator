"""Conservative, schema-checked evidence gate for Ω-GROWER."""
from numbers import Real
from typing import Any
import math

REQUIRED={"prediction_error","null_error","controls_pass","falsification_attempted","uncertainty_reported"}

def evaluate(record:dict[str,Any])->str:
    missing=REQUIRED.difference(record)
    if missing: return "INVALID"
    for key in ("prediction_error","null_error"):
        value=record[key]
        if isinstance(value,bool) or not isinstance(value,Real): return "INVALID"
        if isinstance(value,float) and not math.isfinite(value): return "INVALID"
        if value<0: return "INVALID"
    for key in ("controls_pass","falsification_attempted","uncertainty_reported"):
        if not isinstance(record[key],bool): return "INVALID"
    if not record["falsification_attempted"] or not record["uncertainty_reported"]: return "NOT_PROVEN"
    if not record["controls_pass"]: return "FAIL"
    if record["prediction_error"]<record["null_error"]: return "SUPPORTED"
    return "NOT_PROVEN"

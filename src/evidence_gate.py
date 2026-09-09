"""Conservative evidence gates for Ω-GROWER."""
from typing import Any


def evaluate(record: dict[str, Any]) -> str:
    """Classify one completed test without promoting universal truth."""
    required = {"prediction_error", "null_error", "controls_pass", "falsification_attempted", "uncertainty_reported"}
    missing = required.difference(record)
    if missing:
        return "INVALID"
    if not record["falsification_attempted"] or not record["uncertainty_reported"]:
        return "NOT_PROVEN"
    if not record["controls_pass"]:
        return "FAIL"
    if record["prediction_error"] < record["null_error"]:
        return "SUPPORTED"
    return "NOT_PROVEN"

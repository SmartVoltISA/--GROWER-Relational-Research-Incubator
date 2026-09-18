"""Minimal deterministic Ω-GROWER state core."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from evidence_gate import evaluate as evaluate_evidence


class Status(str, Enum):
    CANDIDATE = "CANDIDATE"
    TESTING = "TESTING"
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    NOT_PROVEN = "NOT_PROVEN"
    FAIL = "FAIL"
    INVALID = "INVALID"
    ARCHIVED = "ARCHIVED"


@dataclass(frozen=True)
class Relation:
    source: str
    relation: str
    target: str
    value: Any = None
    provenance: str = ""


@dataclass
class Hypothesis:
    id: str
    claim: str
    null_hypothesis: str
    predictions: list[str] = field(default_factory=list)
    status: Status = Status.CANDIDATE


@dataclass
class GrowthCycle:
    cycle_id: str
    goal: str
    relations: list[Relation] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    status: Status = Status.CANDIDATE

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        if any(h.id == hypothesis.id for h in self.hypotheses):
            raise ValueError(f"duplicate hypothesis: {hypothesis.id}")
        self.hypotheses.append(hypothesis)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "status" and hasattr(self, "status"):
            raise AttributeError("status is controlled by GrowthCycle transitions")
        object.__setattr__(self, name, value)

    def _set_status(self, status: Status) -> None:
        object.__setattr__(self, "status", status)

    def lock_for_testing(self) -> None:
        if self.status not in {Status.CANDIDATE, Status.PARTIAL, Status.NOT_PROVEN}:
            raise ValueError(f"cannot start testing from state {self.status}")
        if not self.goal.strip():
            raise ValueError("goal is required")
        if not self.relations:
            raise ValueError("at least one relation is required")
        if len(self.hypotheses) < 2:
            raise ValueError("at least two competing hypotheses are required")
        if any(not h.null_hypothesis.strip() for h in self.hypotheses):
            raise ValueError("every hypothesis requires a null hypothesis")
        self._set_status(Status.TESTING)

    def record_evidence(self, record: dict[str, Any]) -> None:
        if self.status not in {Status.TESTING, Status.PARTIAL, Status.NOT_PROVEN}:
            raise ValueError(f"cannot add evidence in state {self.status}")
        if record.get("type") == "test_result":
            raise PermissionError("test results must enter through record_test_result")
        self.evidence.append(dict(record))

    def record_test_result(self, record: dict[str, Any], *, boundary_status: str = "UNKNOWN") -> str:
        """Evaluate evidence centrally before any SUPPORTED decision."""
        allowed_boundary = {"ADMISSIBLE", "FAIL", "NOT_PROVEN", "BOUNDARY_REVIEW_REQUIRED", "UNKNOWN"}
        if boundary_status not in allowed_boundary:
            raise ValueError(f"invalid boundary status: {boundary_status}")
        evidence_status = evaluate_evidence(record)
        entry = dict(record)
        entry.update({
            "type": "test_result",
            "evidence_status": evidence_status,
            "boundary_status": boundary_status,
        })
        if self.status not in {Status.TESTING, Status.PARTIAL, Status.NOT_PROVEN}:
            raise ValueError(f"cannot record test result in state {self.status}")
        self.evidence.append(entry)
        return evidence_status

    def decide(self, status: Status, reason: str) -> None:
        allowed = {Status.SUPPORTED, Status.PARTIAL, Status.NOT_PROVEN, Status.FAIL, Status.INVALID, Status.ARCHIVED}
        if status not in allowed:
            raise ValueError(f"invalid terminal decision: {status}")
        if self.status in {Status.SUPPORTED, Status.FAIL, Status.INVALID, Status.ARCHIVED}:
            raise ValueError(f"terminal cycle cannot transition from {self.status}")
        if not reason.strip():
            raise ValueError("decision reason is required")
        if status is Status.SUPPORTED:
            supported = any(
                e.get("type") == "test_result"
                and e.get("evidence_status") == "SUPPORTED"
                and e.get("boundary_status") == "ADMISSIBLE"
                for e in self.evidence
            )
            if not supported:
                raise PermissionError("SUPPORTED requires a centrally evaluated evidence result and ADMISSIBLE boundary")
        self.evidence.append({"type": "decision", "status": status.value, "reason": reason})
        self._set_status(status)

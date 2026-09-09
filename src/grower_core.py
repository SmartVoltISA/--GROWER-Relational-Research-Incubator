"""Minimal deterministic Ω-GROWER state core.

This module intentionally does not contain a domain solver. It manages
research lineage, hypotheses, evidence and conservative promotion.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


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

    def lock_for_testing(self) -> None:
        if not self.goal.strip():
            raise ValueError("goal is required")
        if not self.relations:
            raise ValueError("at least one relation is required")
        if len(self.hypotheses) < 2:
            raise ValueError("at least two competing hypotheses are required")
        if any(not h.null_hypothesis.strip() for h in self.hypotheses):
            raise ValueError("every hypothesis requires a null hypothesis")
        self.status = Status.TESTING

    def record_evidence(self, record: dict[str, Any]) -> None:
        if self.status not in {Status.TESTING, Status.PARTIAL, Status.NOT_PROVEN}:
            raise ValueError(f"cannot add evidence in state {self.status}")
        self.evidence.append(dict(record))

    def decide(self, status: Status, reason: str) -> None:
        allowed = {Status.SUPPORTED, Status.PARTIAL, Status.NOT_PROVEN, Status.FAIL, Status.INVALID, Status.ARCHIVED}
        if status not in allowed:
            raise ValueError(f"invalid terminal decision: {status}")
        if not reason.strip():
            raise ValueError("decision reason is required")
        self.evidence.append({"type": "decision", "status": status.value, "reason": reason})
        self.status = status

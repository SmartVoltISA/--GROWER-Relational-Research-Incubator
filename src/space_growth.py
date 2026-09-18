"""Controlled SPACE candidate growth from relational seeds."""
from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any

from boundary_gate import evaluate


@dataclass(frozen=True)
class SpaceCandidate:
    candidate_id: str
    parent: str
    goal: str
    organs: tuple[str, ...]
    support_nodes: tuple[str, ...]
    relations: tuple[tuple[str, str, str], ...]
    invariants: tuple[str, ...]
    status: str

    def manifest(self) -> dict[str, Any]:
        return asdict(self)


def grow_space(parent: str = "SPACE-PRODUCT-baseline") -> SpaceCandidate:
    organs = (
        "CORE", "COGNITION", "MEMORY", "GRAPH", "FEEDBACK",
        "GUARDIAN", "RESEARCH", "OBSERVATION", "PLANNING", "ACTION",
        "VISION", "HEARING", "TOUCH", "ENVIRONMENT", "COMPUTER", "DEVICE",
    )
    support_nodes = ("PLAN", "CANDIDATE", "HUMAN_GATE", "PROMOTION")
    relations = (
        ("CORE", "contains", "MEMORY"),
        ("CORE", "contains", "GRAPH"),
        ("COGNITION", "proposes", "PLAN"),
        ("PLAN", "passes_through", "GUARDIAN"),
        ("GUARDIAN", "authorizes", "ACTION"),
        ("OBSERVATION", "feeds", "MEMORY"),
        ("FEEDBACK", "corrects", "CANDIDATE"),
        ("RESEARCH", "tests", "CANDIDATE"),
        ("HUMAN_GATE", "controls", "PROMOTION"),
    )
    if set(organs) & set(support_nodes):
        raise ValueError("organ and support-node namespaces must be disjoint")
    invariants = (
        "identity", "cognition_authority", "guardian_authority",
        "no_self_replication", "no_authority_escalation",
        "canonical_space_immutable", "traceable_branches",
        "evidence_required", "human_gate",
    )
    seed = parent + "|" + "|".join(":" .join(r) for r in relations)
    candidate_id = "SPACE-CANDIDATE-" + sha256(seed.encode()).hexdigest()[:12]
    decision = evaluate({
        "falsification_attempted": False,
        "controls_pass": False,
        "uncertainty_reported": False,
    })
    return SpaceCandidate(
        candidate_id, parent,
        "grow controlled SPACE from relational architecture",
        organs, support_nodes, relations, invariants, decision.status,
    )


if __name__ == "__main__":
    import json
    print(json.dumps(grow_space().manifest(), indent=2, ensure_ascii=False))

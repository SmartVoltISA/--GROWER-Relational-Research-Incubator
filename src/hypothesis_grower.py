"""Small hypothesis-growth engine.

It creates competing, explicitly falsifiable candidates from typed relations.
It never treats generated hypotheses as evidence.
"""
from dataclasses import dataclass
from grower_core import Hypothesis, Relation


@dataclass(frozen=True)
class Candidate:
    hypothesis: Hypothesis
    derivation: str


def grow_hypotheses(relations: list[Relation], prefix: str = "H") -> list[Candidate]:
    if not relations:
        raise ValueError("at least one relation is required")
    out: list[Candidate] = []
    for i, r in enumerate(relations, 1):
        forward = f"{r.source} affects {r.target} through {r.relation}"
        reverse = f"{r.target} affects {r.source} through {r.relation}"
        out.append(Candidate(Hypothesis(f"{prefix}{2*i-1}", forward, f"No directional effect from {r.source} to {r.target}"), "forward relation"))
        out.append(Candidate(Hypothesis(f"{prefix}{2*i}", reverse, f"No directional effect from {r.target} to {r.source}"), "reverse relation"))
    return out

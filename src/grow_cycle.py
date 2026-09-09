"""Deterministic growth-cycle orchestration for Ω-GROWER.

The orchestrator plans; it does not pretend to discover truth. Domain
execution, measurement, and interpretation remain explicit external steps.
"""
from dataclasses import dataclass, field
from typing import Any
from grower_core import GrowthCycle, Hypothesis, Relation, Status


@dataclass
class GrowthResult:
    cycle: GrowthCycle
    next_actions: list[str] = field(default_factory=list)


def seed_cycle(cycle_id: str, goal: str, relations: list[Relation], hypotheses: list[Hypothesis]) -> GrowthCycle:
    cycle = GrowthCycle(cycle_id=cycle_id, goal=goal, relations=list(relations))
    for hypothesis in hypotheses:
        cycle.add_hypothesis(hypothesis)
    cycle.lock_for_testing()
    return cycle


def propose_test_plan(cycle: GrowthCycle) -> list[dict[str, Any]]:
    if cycle.status != Status.TESTING:
        raise ValueError("cycle must be TESTING")
    return [
        {"type": "negative_control", "purpose": "check whether the observed effect can arise under the null"},
        {"type": "discrimination_test", "purpose": "separate competing hypotheses on held-out observations"},
        {"type": "falsification", "purpose": "search actively for a counterexample to each surviving claim"},
        {"type": "reproducibility", "purpose": "repeat with an independent seed/setup when feasible"},
    ]


def attach_observation(cycle: GrowthCycle, observation: dict[str, Any]) -> GrowthCycle:
    required = {"id", "protocol", "result", "uncertainty"}
    missing = required.difference(observation)
    if missing:
        raise ValueError(f"observation missing fields: {sorted(missing)}")
    cycle.record_evidence({"type": "observation", **observation})
    return cycle


def grow(cycle: GrowthCycle) -> GrowthResult:
    """Return the next explicit actions; never auto-promote a claim."""
    if cycle.status not in {Status.TESTING, Status.PARTIAL, Status.NOT_PROVEN}:
        raise ValueError(f"cannot grow from state {cycle.status}")
    actions = ["inspect_evidence", "attempt_falsification", "check_controls", "retest_or_archive"]
    return GrowthResult(cycle=cycle, next_actions=actions)

"""Branch selection and stopping logic for Ω-GROWER.

Selection is deterministic and evidence-aware. It ranks work; it never
turns ranking into truth and never performs automatic promotion.
"""
from dataclasses import dataclass
from typing import Iterable
from grower_core import Status


@dataclass(frozen=True)
class Branch:
    branch_id: str
    status: Status
    evidence_count: int = 0
    falsification_attempted: bool = False
    controls_passed: bool = False
    uncertainty_reported: bool = False


def priority(branch: Branch) -> tuple[int, int, int, int]:
    """Higher tuple = more useful next research target."""
    if branch.status in {Status.FAIL, Status.INVALID, Status.ARCHIVED}:
        return (-100, 0, 0, 0)
    return (
        3 if branch.status == Status.TESTING else 2 if branch.status in {Status.CANDIDATE, Status.NOT_PROVEN, Status.PARTIAL} else 0,
        1 if not branch.falsification_attempted else 0,
        1 if not branch.controls_passed else 0,
        branch.evidence_count,
    )


def select_next(branches: Iterable[Branch]) -> Branch | None:
    active = [b for b in branches if b.status not in {Status.FAIL, Status.INVALID, Status.ARCHIVED, Status.SUPPORTED}]
    return max(active, key=priority, default=None)


def should_stop(branch: Branch) -> tuple[bool, str]:
    if branch.status in {Status.FAIL, Status.INVALID, Status.ARCHIVED}:
        return True, "branch is terminal"
    if not branch.falsification_attempted:
        return False, "falsification required"
    if not branch.controls_passed:
        return False, "controls require resolution"
    if not branch.uncertainty_reported:
        return False, "uncertainty required"
    return True, "research gate satisfied; external promotion decision remains required"

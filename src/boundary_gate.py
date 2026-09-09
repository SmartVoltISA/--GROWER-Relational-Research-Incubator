"""Hard growth boundary for Ω-GROWER.

The gate separates search freedom from authority. Candidates may change
inside the declared boundary, but a candidate cannot change that boundary
and then use the new boundary to justify its own promotion.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BoundaryDecision:
    status: str
    reasons: tuple[str, ...]
    boundary_change_proposed: bool = False


PROTECTED_INVARIANTS = (
    "identity",
    "cognition_authority",
    "guardian_authority",
    "no_self_replication",
    "no_authority_escalation",
    "canonical_space_immutable",
    "traceable_branches",
    "evidence_required",
    "human_gate",
)


def evaluate(candidate: dict[str, Any], *, human_boundary_approval: bool = False) -> BoundaryDecision:
    """Evaluate admissibility without auto-promoting the candidate."""
    reasons: list[str] = []
    violations = set(candidate.get("invariant_violations", ()))
    violations.update(candidate.get("boundary_violations", ()))
    if candidate.get("guardian_bypass_success", False):
        violations.add("guardian_authority")
    if candidate.get("canonical_space_mutated", False):
        violations.add("canonical_space_immutable")

    unknown = violations.difference(PROTECTED_INVARIANTS)
    if unknown:
        reasons.append(f"unknown protected violation(s): {sorted(unknown)}")
    if violations:
        reasons.append(f"protected invariant violation(s): {sorted(violations)}")
        return BoundaryDecision("FAIL", tuple(reasons), bool(candidate.get("boundary_change_proposed", False)))

    boundary_change = bool(candidate.get("boundary_change_proposed", False))
    if boundary_change and not human_boundary_approval:
        return BoundaryDecision(
            "BOUNDARY_REVIEW_REQUIRED",
            ("candidate proposes a boundary change; Human Gate approval is required",),
            True,
        )

    if not candidate.get("falsification_attempted", False):
        return BoundaryDecision("NOT_PROVEN", ("falsification has not been attempted",), boundary_change)
    if not candidate.get("controls_pass", False):
        return BoundaryDecision("NOT_PROVEN", ("required controls have not passed",), boundary_change)
    if not candidate.get("uncertainty_reported", False):
        return BoundaryDecision("NOT_PROVEN", ("uncertainty has not been reported",), boundary_change)

    return BoundaryDecision("ADMISSIBLE", ("candidate remains inside the protected growth boundary",), boundary_change)

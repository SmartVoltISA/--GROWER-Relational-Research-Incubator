"""Hard growth boundary for Ω-GROWER.

Protected boundary changes require an external, target-bound one-shot
OperatorAuthority authorization. A boolean approval flag is deliberately
not accepted.
"""
from dataclasses import dataclass
from typing import Any

from operator_authority import OperatorAuthority, SurgeryAuthorization, SurgeryRequest, ProtectedTarget

@dataclass(frozen=True)
class BoundaryDecision:
    status: str
    reasons: tuple[str, ...]
    boundary_change_proposed: bool = False

PROTECTED_INVARIANTS = (
    "identity", "cognition_authority", "guardian_authority",
    "no_self_replication", "no_authority_escalation",
    "canonical_space_immutable", "traceable_branches",
    "evidence_required", "human_gate",
)

def evaluate(
    candidate: dict[str, Any],
    *,
    operator_authority: OperatorAuthority | None = None,
    operator_authorization: SurgeryAuthorization | None = None,
    surgery_request: SurgeryRequest | None = None,
) -> BoundaryDecision:
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
    if boundary_change:
        if not (operator_authority and operator_authorization and surgery_request):
            return BoundaryDecision(
                "BOUNDARY_REVIEW_REQUIRED",
                ("protected boundary change requires external OperatorAuthority authorization",),
                True,
            )
        if surgery_request.target is not ProtectedTarget.GROWTH_BOUNDARY:
            return BoundaryDecision("FAIL", ("authorization target is not GROWTH_BOUNDARY",), True)
        try:
            operator_authority.consume(operator_authorization, surgery_request)
        except PermissionError as exc:
            return BoundaryDecision("FAIL", (str(exc),), True)

    if not candidate.get("falsification_attempted", False):
        return BoundaryDecision("NOT_PROVEN", ("falsification has not been attempted",), boundary_change)
    if not candidate.get("controls_pass", False):
        return BoundaryDecision("NOT_PROVEN", ("required controls have not passed",), boundary_change)
    if not candidate.get("uncertainty_reported", False):
        return BoundaryDecision("NOT_PROVEN", ("uncertainty has not been reported",), boundary_change)

    return BoundaryDecision("ADMISSIBLE", ("candidate remains inside the protected growth boundary",), boundary_change)

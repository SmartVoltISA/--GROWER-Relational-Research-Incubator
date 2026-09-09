"""Conservative assembly of verified research components."""
from dataclasses import dataclass
from grower_core import Status


@dataclass(frozen=True)
class Component:
    component_id: str
    status: Status
    evidence_ids: tuple[str, ...]
    domain: str
    assumptions: tuple[str, ...] = ()


def assemble(components: list[Component], target: str) -> dict:
    if not target.strip():
        raise ValueError("assembly target is required")
    if not components:
        raise ValueError("at least one component is required")
    bad = [c.component_id for c in components if c.status != Status.SUPPORTED]
    if bad:
        raise ValueError(f"only SUPPORTED components may be assembled: {bad}")
    if any(not c.evidence_ids for c in components):
        raise ValueError("every component requires evidence")
    return {
        "target": target,
        "components": [c.component_id for c in components],
        "domains": sorted({c.domain for c in components}),
        "assumptions": sorted({a for c in components for a in c.assumptions}),
        "evidence_ids": sorted({e for c in components for e in c.evidence_ids}),
        "status": "ASSEMBLED",
        "promotion": "EXTERNAL_HUMAN_DECISION_REQUIRED",
    }

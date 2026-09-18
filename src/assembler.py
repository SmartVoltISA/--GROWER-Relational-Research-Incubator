"""Conservative assembly of verified research components.

Assembly accepts only a certificate minted by a GrowthCycle after its
central evidence and boundary gates have produced SUPPORTED/ADMISSIBLE.
"""
from dataclasses import dataclass
import hashlib
import json
from grower_core import GrowthCycle, Status

_CERTIFICATE_ISSUER = object()


@dataclass(frozen=True)
class VerificationCertificate:
    cycle_id: str
    evidence_id: str
    evidence_fingerprint: str
    input_fingerprint: str
    _issuer: object


@dataclass(frozen=True)
class Component:
    component_id: str
    status: Status
    evidence_ids: tuple[str, ...]
    domain: str
    assumptions: tuple[str, ...] = ()
    certificate: VerificationCertificate | None = None
    cycle_id: str | None = None


def issue_certificate(cycle: GrowthCycle, evidence_id: str) -> VerificationCertificate:
    if cycle.status is not Status.SUPPORTED:
        raise PermissionError("certificate requires SUPPORTED cycle")
    if not cycle._inputs_unchanged():
        raise PermissionError("cycle inputs were modified after verification")
    matches = [
        e for e in cycle.evidence
        if e.get("type") == "test_result"
        and e.get("evidence_status") == "SUPPORTED"
        and e.get("boundary_status") == "ADMISSIBLE"
        and e.get("_cycle_id") == cycle.cycle_id
        and e.get("_evidence_issuer") is cycle._evidence_issuer
    ]
    matches = [e for e in matches if e.get("_fingerprint") == hashlib.sha256(
        json.dumps({k:v for k,v in e.items() if k not in {"_evidence_issuer","_fingerprint"}},
                   sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()]
    match = next((e for e in matches if evidence_id == e.get("evidence_id")), None)
    if match is None:
        raise PermissionError("certificate evidence is not a supported gated result")
    return VerificationCertificate(cycle.cycle_id, evidence_id, match["_fingerprint"], cycle._locked_fingerprint or "", _CERTIFICATE_ISSUER)


def assemble(components: list[Component], target: str) -> dict:
    if not target.strip():
        raise ValueError("assembly target is required")
    if not components:
        raise ValueError("at least one component is required")
    for c in components:
        if c.status != Status.SUPPORTED:
            raise ValueError(f"only SUPPORTED components may be assembled: {c.component_id}")
        if not c.evidence_ids or c.certificate is None:
            raise ValueError("every component requires a verified certificate")
        if c.certificate._issuer is not _CERTIFICATE_ISSUER:
            raise PermissionError("invalid certificate")
        if not c.cycle_id or c.certificate.cycle_id != c.cycle_id:
            raise PermissionError("certificate is not bound to component cycle")
        if c.certificate.evidence_id not in c.evidence_ids:
            raise PermissionError("certificate evidence is not bound to component")
        if any(not isinstance(e, str) or not e.strip() for e in c.evidence_ids):
            raise ValueError("component evidence IDs must be non-empty strings")
        if len(set(c.evidence_ids)) != len(c.evidence_ids):
            raise ValueError("component evidence IDs must be unique")
        if not c.certificate.evidence_fingerprint.strip():
            raise PermissionError("certificate evidence fingerprint is required")
        if not c.certificate.input_fingerprint.strip():
            raise PermissionError("certificate input fingerprint is required")
    return {
        "target": target,
        "components": [c.component_id for c in components],
        "domains": sorted({c.domain for c in components}),
        "assumptions": sorted({a for c in components for a in c.assumptions}),
        "evidence_ids": sorted({e for c in components for e in c.evidence_ids}),
        "status": "ASSEMBLED",
        "promotion": "EXTERNAL_HUMAN_DECISION_REQUIRED",
    }

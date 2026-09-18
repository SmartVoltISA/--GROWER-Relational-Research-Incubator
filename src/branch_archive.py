"""Tamper-evident append-only branch archive.

The legacy archive_branch(record, list) API remains for compatibility, while
AppendOnlyArchive provides the canonical integrity-bound storage boundary.
"""
from dataclasses import dataclass, asdict
from typing import Any
import hashlib
import json

TERMINAL_ARCHIVE_STATUSES = frozenset({"FAIL", "INVALID", "ARCHIVED", "NOT_PROVEN"})


@dataclass(frozen=True)
class BranchRecord:
    branch_id: str
    parent_id: str | None
    status: str
    reason: str
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in TERMINAL_ARCHIVE_STATUSES:
            raise ValueError(f"only terminal/rejected branches may be archived: {self.status}")
        if not isinstance(self.branch_id, str) or not self.branch_id.strip() or not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("branch_id and reason are required")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("evidence_ids must be unique")


def serialize(record: BranchRecord) -> str:
    return json.dumps(asdict(record), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class AppendOnlyArchive:
    """Canonical in-process archive with hash-linked immutable entries."""

    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []
        self._head = "GENESIS"

    @property
    def head(self) -> str:
        return self._head

    def append(self, record: BranchRecord) -> str:
        if any(e["branch_id"] == record.branch_id for e in self._entries):
            raise ValueError(f"duplicate archived branch: {record.branch_id}")
        payload = {
            "branch": asdict(record),
            "previous": self._head,
        }
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode()).hexdigest()
        entry = {
            "branch_id": record.branch_id,
            "record": asdict(record),
            "previous": self._head,
            "fingerprint": digest,
        }
        self._entries.append(entry)
        self._head = digest
        return digest

    def verify(self) -> bool:
        previous = "GENESIS"
        seen: set[str] = set()
        for entry in self._entries:
            if entry["branch_id"] in seen:
                return False
            seen.add(entry["branch_id"])
            payload = {"branch": entry["record"], "previous": previous}
            canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            if hashlib.sha256(canonical.encode()).hexdigest() != entry["fingerprint"]:
                return False
            previous = entry["fingerprint"]
        return previous == self._head

    def records(self) -> tuple[dict[str, Any], ...]:
        return tuple({
            "branch_id": e["branch_id"],
            "record": dict(e["record"]),
            "previous": e["previous"],
            "fingerprint": e["fingerprint"],
        } for e in self._entries)


def archive_branch(record: BranchRecord, archive: list[dict[str, Any]]) -> None:
    """Legacy compatibility API; not canonical tamper-evident storage."""
    if any(x.get("branch_id") == record.branch_id for x in archive):
        raise ValueError(f"duplicate archived branch: {record.branch_id}")
    archive.append(asdict(record))

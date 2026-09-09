"""Immutable-style branch records for failed and rejected growth paths."""
from dataclasses import dataclass, asdict
from typing import Any
import json


@dataclass(frozen=True)
class BranchRecord:
    branch_id: str
    parent_id: str | None
    status: str
    reason: str
    evidence_ids: tuple[str, ...] = ()


def serialize(record: BranchRecord) -> str:
    return json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)


def archive_branch(record: BranchRecord, archive: list[dict[str, Any]]) -> None:
    if any(x.get("branch_id") == record.branch_id for x in archive):
        raise ValueError(f"duplicate archived branch: {record.branch_id}")
    archive.append(asdict(record))

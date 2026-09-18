import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from branch_archive import AppendOnlyArchive, BranchRecord

def test_append_only_archive_verifies_chain():
    archive = AppendOnlyArchive()
    a = archive.append(BranchRecord("B1", None, "FAIL", "f1", ("E1",)))
    b = archive.append(BranchRecord("B2", "B1", "ARCHIVED", "f2"))
    assert a != b
    assert archive.verify() is True

def test_append_only_archive_rejects_replay():
    archive = AppendOnlyArchive()
    record = BranchRecord("B1", None, "FAIL", "f1")
    archive.append(record)
    try:
        archive.append(record)
    except ValueError:
        pass
    else:
        raise AssertionError("archived branch replay accepted")

def test_append_only_archive_detects_tampering():
    archive = AppendOnlyArchive()
    archive.append(BranchRecord("B1", None, "FAIL", "f1"))
    archive._entries[0]["record"]["reason"] = "rewritten"
    assert archive.verify() is False

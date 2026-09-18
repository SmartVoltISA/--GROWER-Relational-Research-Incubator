import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from branch_archive import BranchRecord, archive_branch, serialize

def test_archive_record_is_detached_from_input():
    archive=[]
    record=BranchRecord("B1","P1","FAIL","failed",("E1",))
    archive_branch(record,archive)
    record2=BranchRecord("B2","P1","NOT_PROVEN","pending",("E2",))
    archive_branch(record2,archive)
    record2_evidence=list(record2.evidence_ids)
    record2_evidence.append("FAKE")
    assert archive[1]["evidence_ids"]==("E2",)
    assert serialize(record2).find("FAKE")==-1

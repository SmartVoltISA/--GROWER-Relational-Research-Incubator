import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from grower_core import GrowthCycle,Hypothesis,Relation,Status
from branch_archive import BranchRecord,archive_branch

def test_terminal_cycle_cannot_be_reopened_by_lock():
    c=GrowthCycle("REC-1","test",[Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A")); c.add_hypothesis(Hypothesis("H2","B","not B"))
    c.lock_for_testing(); c.decide(Status.FAIL,"falsified")
    try: c.lock_for_testing()
    except ValueError: pass
    else: raise AssertionError("terminal cycle reopened")

def test_archived_branch_id_cannot_be_replayed():
    archive=[]
    r=BranchRecord("B1","P","FAIL","falsified",())
    archive_branch(r,archive)
    try: archive_branch(r,archive)
    except ValueError: pass
    else: raise AssertionError("archived branch replay accepted")

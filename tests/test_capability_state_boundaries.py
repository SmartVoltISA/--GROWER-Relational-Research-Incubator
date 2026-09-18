import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from capability_state import CapabilityState

def test_snapshot_is_detached_from_state():
    c=CapabilityState({"A"},{"A"},["A"],set())
    s=c.snapshot()
    s["CAN"].append("B")
    s["DID"].append("FAKE")
    assert c.allowed("B") is False
    assert c.did==["A"]

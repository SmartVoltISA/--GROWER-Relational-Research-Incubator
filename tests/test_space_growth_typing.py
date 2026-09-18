import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from space_growth import grow_space


def test_space_candidate_has_typed_namespaces():
    c = grow_space()
    assert len(c.organs) == 16
    assert c.support_nodes
    assert not set(c.organs) & set(c.support_nodes)
    assert {"HUMAN_GATE", "PROMOTION"} <= set(c.support_nodes)

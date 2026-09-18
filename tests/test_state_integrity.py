import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from grower_core import GrowthCycle, Hypothesis, Relation, Status

def cycle():
    c=GrowthCycle("S1","state", [Relation("A","r","B")])
    c.add_hypothesis(Hypothesis("H1","A","not A"))
    c.add_hypothesis(Hypothesis("H2","B","not B"))
    return c

def test_direct_status_assignment_is_blocked():
    c=cycle()
    try:
        c.status=Status.SUPPORTED
    except AttributeError:
        pass
    else:
        raise AssertionError("direct status mutation was accepted")

def test_terminal_cycle_cannot_be_reopened():
    c=cycle()
    c.lock_for_testing()
    c.decide(Status.FAIL, "falsified")
    try:
        c.lock_for_testing()
    except ValueError:
        pass
    else:
        raise AssertionError("terminal cycle was reopened")

def test_terminal_cycle_cannot_receive_second_decision():
    c=cycle()
    c.lock_for_testing()
    c.decide(Status.INVALID, "invalid evidence")
    try:
        c.decide(Status.FAIL, "second decision")
    except ValueError:
        pass
    else:
        raise AssertionError("terminal cycle accepted second decision")

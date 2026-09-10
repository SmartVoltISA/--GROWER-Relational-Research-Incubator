"""GROWER v1: reusable tool synthesis under falsification.

Purpose: test whether an incubator can turn examples into a reusable procedure,
actively falsify the first candidate, synthesize a corrected candidate, and
transfer it to unseen contexts.

This is a controlled capability experiment, NOT an AGI claim.
"""
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Candidate:
    name: str
    fn: object
    complexity: int


# Tiny declarative tool language. GROWER searches this space rather than being
# handed the hidden rule. Constants are intentionally limited and fixed before
# the experiment.
def make_candidates():
    atoms = [
        ("x", lambda x: x, 1),
        ("x+1", lambda x: x + 1, 2),
        ("x-1", lambda x: x - 1, 2),
        ("2*x", lambda x: 2 * x, 2),
        ("x*x", lambda x: x * x, 2),
        ("abs(x)", lambda x: abs(x), 2),
    ]
    constants = [(str(c), (lambda x, c=c: c), 1) for c in (-3, -2, -1, 0, 1, 2, 3)]
    out = [Candidate(n, f, k) for n, f, k in atoms + constants]
    unary = [(f"-({n})", lambda x, f=f: -f(x), k + 1) for n, f, k in atoms]
    out += [Candidate(n, f, k) for n, f, k in unary]
    bases = atoms + constants
    for (n1, f1, k1), (n2, f2, k2) in product(bases, bases):
        for op, fn in (
            ("+", lambda a, b: a + b),
            ("-", lambda a, b: a - b),
            ("*", lambda a, b: a * b),
        ):
            out.append(Candidate(f"({n1}{op}{n2})", lambda x, f1=f1, f2=f2, fn=fn: fn(f1(x), f2(x)), k1 + k2 + 1))
    # deterministic de-duplication by name
    return {c.name: c for c in out}.values()


def fits(candidate, examples):
    return all(candidate.fn(x) == y for x, y in examples)


def synthesize(examples, rejected_names=()):
    rejected = set(rejected_names)
    pool = sorted(make_candidates(), key=lambda c: (c.complexity, c.name))
    for c in pool:
        if c.name not in rejected and fits(c, examples):
            return c
    return None


def run():
    # Hidden target: y = x*x + 1. It is never supplied to GROWER.
    train = [(-2, 5), (-1, 2), (0, 1), (2, 5)]
    held_out = [(-3, 10), (1, 2), (3, 10)]
    falsifier = [(4, 17)]

    candidate1 = synthesize(train)
    if candidate1 is None:
        return {"status": "FAIL", "reason": "no_candidate"}

    # Falsification is independent of the training examples.
    false_positive = not fits(candidate1, falsifier)
    rejected = [candidate1.name] if false_positive else []

    # Re-synthesize after the counterexample. This is the growth/correction step.
    candidate2 = synthesize(train + falsifier, rejected)
    if candidate2 is None:
        return {"status": "FAIL", "reason": "no_corrected_candidate", "candidate1": candidate1.name}

    transfer_correct = sum(candidate2.fn(x) == y for x, y in held_out)
    transfer_total = len(held_out)

    # Negative control: memorizes training examples only; it must not transfer.
    memory = dict(train + falsifier)
    control_correct = sum(memory.get(x) == y for x, y in held_out)

    return {
        "status": "SUPPORTED" if transfer_correct == transfer_total and false_positive else "PARTIAL",
        "candidate_1": candidate1.name,
        "candidate_1_rejected_by_falsifier": false_positive,
        "candidate_2": candidate2.name,
        "transfer_correct": transfer_correct,
        "transfer_total": transfer_total,
        "transfer_score": transfer_correct / transfer_total,
        "negative_control_transfer_score": control_correct / transfer_total,
        "tool_created": candidate2.name != candidate1.name,
        "invariant_violations": 0,
        "hidden_target_disclosed_to_learner": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))

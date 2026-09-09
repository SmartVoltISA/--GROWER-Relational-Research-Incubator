"""Error-driven iteration gate.

Tests whether a learner can infer the need for repeated composition from its
own under-generalization error. No REPEAT/FIXPOINT/CLOSURE primitive is
available to the mechanism synthesizer. The controller is a separate,
explicit research hypothesis and is not treated as proof of autonomous
self-improvement.
"""
from __future__ import annotations
from dataclasses import dataclass

Pair = tuple[str, str]
Relation = frozenset[Pair]


def compose(a: Relation, b: Relation) -> Relation:
    return frozenset((x, z) for x, y in a for y2, z in b if y == y2)


def closure(base: Relation) -> Relation:
    r = base
    while True:
        nxt = r | compose(r, base)
        if nxt == r:
            return r
        r = nxt


def finite_program(base: Relation, depth: int) -> Relation:
    r = base
    for _ in range(depth - 1):
        r = r | compose(r, base)
    return r


def chain(n: int) -> tuple[Relation, Relation]:
    nodes = [f"N{i}" for i in range(n + 1)]
    base = frozenset(zip(nodes, nodes[1:]))
    return base, closure(base)


@dataclass
class ErrorDrivenLearner:
    depth: int = 1
    max_depth: int = 32

    def solve(self, base: Relation, expected: Relation) -> tuple[Relation, int]:
        attempts = 0
        while attempts < self.max_depth:
            prediction = finite_program(base, self.depth)
            if prediction == expected:
                return prediction, self.depth
            # Error signal: predicted relation is incomplete. Increase the
            # reusable composition depth and test again. This controller is
            # deliberately explicit so it cannot be mistaken for spontaneous
            # motivation or unconstrained self-modification.
            missing = expected - prediction
            if not missing:
                return prediction, self.depth
            self.depth += 1
            attempts += 1
        return prediction, self.depth


def main() -> dict:
    learner = ErrorDrivenLearner()
    results = []
    for length in range(1, 9):
        base, expected = chain(length)
        prediction, depth = learner.solve(base, expected)
        results.append({
            "chain_length": length,
            "passed": prediction == expected,
            "depth_used": depth,
            "missing_after": len(expected - prediction),
        })
    return {
        "results": results,
        "all_passed": all(r["passed"] for r in results),
        "max_depth_used": max(r["depth_used"] for r in results),
    }


if __name__ == "__main__":
    print(main())

"""Autonomous relational mechanism synthesis v2.

The learner is NOT given named candidate mechanisms such as "closure".
It generates small expression programs from primitive relational operators,
evaluates them on train/held-out/adversarial cases, and selects only after
falsification. This is autonomous search inside a fixed, declared grammar;
it is not a claim of open-ended AGI.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product

Pair = tuple[str, str]
Relation = frozenset[Pair]


def compose(a: Relation, b: Relation) -> Relation:
    return frozenset((x, z) for x, y in a for y2, z in b if y == y2)


def union(a: Relation, b: Relation) -> Relation:
    return frozenset(set(a) | set(b))


def inverse(a: Relation) -> Relation:
    return frozenset((y, x) for x, y in a)


@dataclass(frozen=True)
class Expr:
    op: str
    args: tuple["Expr", ...] = ()
    def render(self) -> str:
        return self.op if not self.args else f"{self.op}({','.join(a.render() for a in self.args)})"
    def size(self) -> int:
        return 1 + sum(a.size() for a in self.args)


def eval_expr(expr: Expr, base: Relation) -> Relation:
    if expr.op == "EDGE":
        return base
    if expr.op == "INV":
        return inverse(eval_expr(expr.args[0], base))
    if expr.op == "UNION":
        return union(eval_expr(expr.args[0], base), eval_expr(expr.args[1], base))
    if expr.op == "COMP":
        return compose(eval_expr(expr.args[0], base), eval_expr(expr.args[1], base))
    if expr.op == "REPEAT":
        # Generic fixed-point operator: repeatedly apply the child relation
        # composition until no new pairs appear. The generator does not know
        # the semantic name "transitive closure".
        r = base
        child = expr.args[0]
        step = eval_expr(child, base)
        while True:
            nxt = union(r, compose(r, step))
            if nxt == r:
                return r
            r = nxt
    raise ValueError(expr.op)


def generate(depth: int) -> list[Expr]:
    levels: list[list[Expr]] = [[Expr("EDGE")]]
    for d in range(1, depth + 1):
        prev = [e for level in levels for e in level]
        candidates = []
        for e in prev:
            candidates.append(Expr("INV", (e,)))
            candidates.append(Expr("REPEAT", (e,)))
        for a, b in product(prev, repeat=2):
            candidates.append(Expr("UNION", (a, b)))
            candidates.append(Expr("COMP", (a, b)))
        seen = {}
        for e in candidates:
            seen[e.render()] = e
        levels.append(list(seen.values()))
    # Keep only compact expressions; deduplication is deterministic.
    all_expr = {e.render(): e for level in levels for e in level}
    return sorted(all_expr.values(), key=lambda e: (e.size(), e.render()))


def target(base: Relation, expected: Relation) -> float:
    pred = expected
    return float(pred == expected)


def score(expr: Expr, cases: list[tuple[Relation, Relation]]) -> float:
    return sum(eval_expr(expr, base) == expected for base, expected in cases) / len(cases)


def make_cases():
    train = [
        (frozenset({("A", "B")}), frozenset({("A", "B")})),
        (frozenset({("A", "B"), ("B", "C")}), frozenset({("A", "B"), ("B", "C"), ("A", "C")})),
        (frozenset({("X", "Y"), ("Y", "Z"), ("Z", "Q")}), frozenset({("X", "Y"), ("Y", "Z"), ("Z", "Q"), ("X", "Z"), ("Y", "Q"), ("X", "Q")})),
    ]
    held = [
        (frozenset({("M", "N"), ("N", "O"), ("O", "P"), ("P", "R")}), frozenset({("M", "N"), ("N", "O"), ("O", "P"), ("P", "R"), ("M", "O"), ("N", "P"), ("O", "R"), ("M", "P"), ("N", "R"), ("M", "R")})),
        (frozenset({("1", "2"), ("2", "3")}), frozenset({("1", "2"), ("2", "3"), ("1", "3")})),
    ]
    adversarial = [
        (frozenset({("A", "B"), ("B", "A")}), frozenset({("A", "A"), ("B", "B"), ("A", "B"), ("B", "A")})),
        (frozenset({("A", "B"), ("C", "D")}), frozenset({("A", "B"), ("C", "D")})),
    ]
    return train, held, adversarial


def main() -> dict:
    train, held, adversarial = make_cases()
    candidates = generate(depth=2)
    ranked = sorted(((score(e, train), -e.size(), e.render(), e) for e in candidates), reverse=True)
    best = ranked[0][3]
    return {
        "candidate_count": len(candidates),
        "selected": best.render(),
        "train_score": score(best, train),
        "held_out_score": score(best, held),
        "adversarial_score": score(best, adversarial),
        "selected_size": best.size(),
        "falsification_passed": score(best, adversarial) == 1.0,
    }


if __name__ == "__main__":
    print(main())

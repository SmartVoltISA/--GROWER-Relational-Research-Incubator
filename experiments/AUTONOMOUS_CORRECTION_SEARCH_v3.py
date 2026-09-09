"""Autonomous correction-strategy search v3.

Purpose
-------
Start from a deliberately failing relational program (EDGE). Do not provide a
correction rule such as "increase depth". Generate competing correction
programs from a declared primitive/control grammar, score them on train data,
then falsify the winner on held-out and adversarial cases.

Important limitation
--------------------
The search space is declared by the experiment. Discovering STABLE(EDGE)
therefore demonstrates selection/synthesis of a useful correction strategy
inside the grammar, not open-ended AGI or invention outside the grammar.

Safety
------
Pure local computation. No network actions, self-modification, replication,
authority changes, or external side effects.
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


def closure(base: Relation, max_iter: int = 100) -> Relation:
    current = base
    for _ in range(max_iter):
        nxt = union(current, compose(current, base))
        if nxt == current:
            return current
        current = nxt
    raise RuntimeError("STABLE did not converge within the declared bound")


@dataclass(frozen=True)
class Program:
    op: str
    child: "Program | None" = None
    k: int | None = None
    left: "Program | None" = None
    right: "Program | None" = None

    def render(self) -> str:
        if self.op == "EDGE":
            return "EDGE"
        if self.op == "INV":
            return f"INV({self.child.render()})"
        if self.op == "STABLE":
            return f"STABLE({self.child.render()})"
        if self.op == "FIXED":
            return f"FIXED{self.k}({self.child.render()})"
        if self.op in {"UNION", "COMP"}:
            return f"{self.op}({self.left.render()},{self.right.render()})"
        raise ValueError(self.op)

    def size(self) -> int:
        return 1 + (self.child.size() if self.child else 0) + (self.left.size() if self.left else 0) + (self.right.size() if self.right else 0)


def evaluate(program: Program, base: Relation) -> Relation:
    if program.op == "EDGE":
        return base
    if program.op == "INV":
        return inverse(evaluate(program.child, base))
    if program.op == "UNION":
        return union(evaluate(program.left, base), evaluate(program.right, base))
    if program.op == "COMP":
        return compose(evaluate(program.left, base), evaluate(program.right, base))
    if program.op == "STABLE":
        return closure(evaluate(program.child, base))
    if program.op == "FIXED":
        current = evaluate(program.child, base)
        for _ in range(program.k - 1):
            current = union(current, compose(current, base))
        return current
    raise ValueError(program.op)


def generate(depth: int = 2, allow_stable: bool = True) -> list[Program]:
    levels: list[list[Program]] = [[Program("EDGE")]]
    for _ in range(depth):
        previous = [p for level in levels for p in level]
        candidates: list[Program] = []
        for child in previous:
            candidates.append(Program("INV", child=child))
            for k in (2, 3, 4, 5, 6, 8):
                candidates.append(Program("FIXED", child=child, k=k))
            if allow_stable:
                candidates.append(Program("STABLE", child=child))
        for left, right in product(previous, repeat=2):
            candidates.append(Program("UNION", left=left, right=right))
            candidates.append(Program("COMP", left=left, right=right))
        levels.append(list({p.render(): p for p in candidates}.values()))
    return sorted({p.render(): p for level in levels for p in level}.values(), key=lambda p: (p.size(), p.render()))


def chain(n: int, prefix: str = "A") -> Relation:
    nodes = [chr(ord(prefix) + i) if i < 26 else f"{prefix}{i}" for i in range(n + 1)]
    return frozenset(zip(nodes, nodes[1:]))


def transitive_closure(base: Relation) -> Relation:
    result = set(base)
    changed = True
    while changed:
        changed = False
        for a, b in list(result):
            for c, d in list(result):
                if b == c and (a, d) not in result:
                    result.add((a, d))
                    changed = True
    return frozenset(result)


def cases():
    train = [(chain(n), transitive_closure(chain(n))) for n in (1, 2, 3, 4, 5, 6)]
    held = [(chain(n, "M"), transitive_closure(chain(n, "M"))) for n in (7, 8, 10)]
    adversarial = [
        (frozenset({("A", "B"), ("B", "A")}), transitive_closure(frozenset({("A", "B"), ("B", "A")}))),
        (frozenset({("A", "B"), ("C", "D")}), transitive_closure(frozenset({("A", "B"), ("C", "D")}))),
        (frozenset({("A", "B"), ("B", "C"), ("D", "E")}), transitive_closure(frozenset({("A", "B"), ("B", "C"), ("D", "E")}))),
    ]
    return train, held, adversarial


def score(program: Program, dataset) -> float:
    return sum(evaluate(program, base) == expected for base, expected in dataset) / len(dataset)


def select(dataset, allow_stable: bool):
    candidates = generate(depth=2, allow_stable=allow_stable)
    ranked = sorted(candidates, key=lambda p: (score(p, dataset), -p.size(), p.render()), reverse=True)
    return ranked[0], len(candidates)


def main() -> dict:
    train, held, adversarial = cases()
    initial = Program("EDGE")
    initial_train = score(initial, train)
    best, count = select(train, allow_stable=True)
    ablation, ablation_count = select(train, allow_stable=False)
    result = {
        "initial_program": initial.render(),
        "initial_train_score": initial_train,
        "correction_search_candidate_count": count,
        "selected_correction_strategy": best.render(),
        "selected_train_score": score(best, train),
        "selected_held_out_score": score(best, held),
        "selected_adversarial_score": score(best, adversarial),
        "selected_size": best.size(),
        "falsification_passed": score(best, adversarial) == 1.0,
        "ablation_without_stable_candidate_count": ablation_count,
        "ablation_selected": ablation.render(),
        "ablation_train_score": score(ablation, train),
        "ablation_held_out_score": score(ablation, held),
        "ablation_adversarial_score": score(ablation, adversarial),
        "generalization_gap_closed": score(best, held) > score(ablation, held),
    }
    return result


if __name__ == "__main__":
    print(main())

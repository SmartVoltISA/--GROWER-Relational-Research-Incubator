"""Gate experiment: tree vs relational network under identical evidence.

Question: does relational redundancy provide more opportunities to detect
inconsistency than a tree, when both receive the same noisy relation evidence?
This is a structural experiment only; it makes no biological claim.
"""
from __future__ import annotations
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    n: int
    tree_constraints: int
    network_constraints: int
    tree_cycles: int
    network_cycles: int
    tree_checks: int
    network_checks: int


def run(n: int = 30, p: float = 0.15, seed: int = 20260909) -> Result:
    rng = random.Random(seed)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
    # Build a connected spanning tree from the same edge pool.
    tree: list[tuple[int, int]] = []
    seen = {0}
    while len(seen) < n:
        candidates = [e for e in edges if (e[0] in seen) ^ (e[1] in seen)]
        if not candidates:
            raise ValueError("generated graph was disconnected")
        e = rng.choice(candidates)
        tree.append(e)
        seen.update(e)
    # For an undirected connected graph, cycle rank = E - V + 1.
    return Result(
        n=n,
        tree_constraints=len(tree),
        network_constraints=len(edges),
        tree_cycles=max(0, len(tree) - n + 1),
        network_cycles=max(0, len(edges) - n + 1),
        tree_checks=max(0, len(tree) - n + 1),
        network_checks=max(0, len(edges) - n + 1),
    )


if __name__ == "__main__":
    for seed in range(20260909, 20261009):
        r = run(seed=seed)
        print(r)

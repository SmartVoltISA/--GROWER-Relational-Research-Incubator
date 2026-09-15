"""Ω Minimal World E0 — deterministic executable scaffold.

This is deliberately a small model for testing the preregistered controls.
It is not a claim of digital life. Run locally and preserve the exact file
used for any reported result.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from collections import deque

N = 100
STEPS = 5000
SEEDS = range(1001, 1021)

@dataclass
class Agent:
    resource: float = 10.0
    state: int = 0
    memory: deque[int] | None = None
    impulse: float = 0.0
    inertia: float = 0.25
    alive: bool = True


def run(condition: str, seed: int) -> dict:
    rng = random.Random(seed)
    agents = [Agent(memory=deque(maxlen=20)) for _ in range(N)]
    edges = {}
    initial_edges = set()
    for i in range(N):
        for j in range(i + 1, N):
            if rng.random() < 0.03:
                edges[(i, j)] = rng.uniform(0.1, 1.0)
                initial_edges.add((i, j))

    persistent = [0] * STEPS
    for t in range(STEPS):
        alive = [i for i, a in enumerate(agents) if a.alive]
        # Fixed environmental budget; abundant-resource control removes scarcity.
        inflow = (N * 0.08) if condition != "ABUNDANT_RESOURCE" else (N * 10.0)
        share = inflow / max(1, len(alive))
        for i in alive:
            a = agents[i]
            a.resource = min(20.0, a.resource + share)
            a.impulse = max(0.0, 1.0 - a.resource / 20.0)

        for i in alive:
            a = agents[i]
            neighbors = [j if i < j else j for (u, j) in edges if u == i] + [u for (u, v) in edges if v == i]
            target = rng.choice(neighbors) if neighbors else None
            desired = a.state
            if target is not None:
                desired = agents[target].state
                if condition != "NO_FEEDBACK" and a.impulse > 0.4:
                    a.resource += 0.02 * edges[(min(i, target), max(i, target))]
            if condition != "NO_MEMORY" and a.memory:
                desired = round((desired + sum(a.memory) / len(a.memory)) / 2)
            if rng.random() < a.inertia:
                desired = a.state
            if a.impulse > 0.6:
                desired = 1 - a.state
            if condition == "NO_FEEDBACK":
                desired = rng.choice((0, 1)) if rng.random() < 0.05 else a.state
            a.state = desired
            a.resource -= 0.03 + 0.02 * a.impulse
            if condition != "NO_MEMORY":
                a.memory.append(a.state)
            if a.resource <= 0:
                a.alive = False

        # Adaptive relation update for FULL; decay otherwise.
        if condition == "FULL":
            for e in list(edges):
                u, v = e
                if agents[u].state == agents[v].state:
                    edges[e] = min(1.0, edges[e] + 0.01)
                else:
                    edges[e] *= 0.995
                if edges[e] < 0.05:
                    del edges[e]
            for _ in range(max(1, len(alive) // 10)):
                u, v = rng.sample(alive, 2) if len(alive) >= 2 else (0, 0)
                if u != v:
                    edges[(min(u, v), max(u, v))] = max(edges.get((min(u, v), max(u, v)), 0.0), 0.1)
        else:
            for e in list(edges):
                edges[e] *= 0.999
                if edges[e] < 0.05:
                    del edges[e]

        persistent[t] = sum(a.alive for a in agents) / N

    surviving_initial = len(initial_edges & set(edges)) / max(1, len(initial_edges))
    return {
        "condition": condition,
        "seed": seed,
        "final_survival": persistent[-1],
        "mean_survival": sum(persistent) / STEPS,
        "edge_count": len(edges),
        "initial_edge_persistence": surviving_initial,
    }


if __name__ == "__main__":
    conditions = ["RANDOM", "NO_MEMORY", "NO_FEEDBACK", "ABUNDANT_RESOURCE", "FULL"]
    print("condition,seed,final_survival,mean_survival,edge_count,initial_edge_persistence")
    for condition in conditions:
        for seed in SEEDS:
            r = run(condition, seed)
            print(",".join(str(r[k]) for k in ("condition", "seed", "final_survival", "mean_survival", "edge_count", "initial_edge_persistence")))

from __future__ import annotations

"""Ω Minimal World E0 v0.2

Deterministic reference implementation for the v0.2 preregistration.
This is a protocol implementation, not evidence. Batch results must be
inspected only after this implementation is frozen.
"""

from dataclasses import dataclass, field
from collections import deque
import math
import random

N = 100
STEPS = 5000
SEEDS = range(1001, 1021)
WORLD_SIZE = 1.0
INTERACTION_RADIUS = 0.16
INITIAL_RESOURCE = 10.0
RESOURCE_CAPACITY = 20.0
BASE_REPLENISHMENT = 0.025
ABUNDANT_REPLENISHMENT = 0.25
CONSUMPTION_BASE = 0.035
MEMORY_LENGTH = 20
RELATION_INITIAL = 0.10
RELATION_REINFORCE = 0.01
RELATION_DECAY = 0.002


@dataclass
class Agent:
    x: float
    y: float
    resource: float = INITIAL_RESOURCE
    state: int = 0
    memory: deque[int] = field(default_factory=lambda: deque(maxlen=MEMORY_LENGTH))
    inertia: float = 0.25
    alive: bool = True
    lifetime: int = 0


def distance(a: Agent, b: Agent) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return math.hypot(dx, dy)


def interaction_pairs(agents: list[Agent]) -> list[tuple[int, int]]:
    alive = [i for i, a in enumerate(agents) if a.alive]
    pairs: list[tuple[int, int]] = []
    for p, i in enumerate(alive):
        for j in alive[p + 1 :]:
            if distance(agents[i], agents[j]) <= INTERACTION_RADIUS:
                pairs.append((i, j))
    return pairs


def resource_transfer(a: Agent, b: Agent) -> float:
    if a.resource > b.resource:
        donor, receiver = a, b
    else:
        donor, receiver = b, a
    surplus = max(0.0, donor.resource - RESOURCE_CAPACITY / 2)
    need = max(0.0, RESOURCE_CAPACITY / 2 - receiver.resource)
    return min(0.05, surplus * 0.05, need * 0.05)


def run(condition: str, seed: int) -> dict:
    rng = random.Random(seed)
    agents = [Agent(rng.random(), rng.random()) for _ in range(N)]
    edges: dict[tuple[int, int], float] = {}
    initial_relation_cohort: set[tuple[int, int]] = set()
    resource_transfers: dict[tuple[int, int], float] = {}
    survival_series: list[float] = []
    giant_series: list[float] = []
    state_series: list[float] = []

    for t in range(STEPS):
        alive = [i for i, a in enumerate(agents) if a.alive]
        if not alive:
            survival_series.append(0.0)
            giant_series.append(0.0)
            state_series.append(0.0)
            continue

        # Shared movement opportunity across every condition.
        for i in alive:
            a = agents[i]
            a.x = min(1.0, max(0.0, a.x + rng.uniform(-0.03, 0.03)))
            a.y = min(1.0, max(0.0, a.y + rng.uniform(-0.03, 0.03)))

        replenishment = ABUNDANT_REPLENISHMENT if condition == "ABUNDANT_RESOURCE" else BASE_REPLENISHMENT
        for i in alive:
            a = agents[i]
            a.resource = min(RESOURCE_CAPACITY, a.resource + replenishment)

        pairs = interaction_pairs(agents)
        touched: set[tuple[int, int]] = set()
        for i, j in pairs:
            e = (i, j)
            touched.add(e)
            old_weight = edges.get(e, RELATION_INITIAL)
            if e not in edges:
                edges[e] = old_weight
                if t == 0:
                    initial_relation_cohort.add(e)

            transfer = resource_transfer(agents[i], agents[j])
            if transfer > 0:
                if agents[i].resource > agents[j].resource:
                    agents[i].resource -= transfer
                    agents[j].resource += transfer
                else:
                    agents[j].resource -= transfer
                    agents[i].resource += transfer
                resource_transfers[e] = resource_transfers.get(e, 0.0) + transfer

            # Only conditions with feedback allow interaction outcome to change state.
            # NO_FEEDBACK still receives the same interaction/resource event, but that
            # event cannot feed back into future internal state or relation adaptation.
            if condition != "NO_FEEDBACK":
                if agents[i].resource < agents[j].resource:
                    agents[i].state = agents[j].state
                elif agents[j].resource < agents[i].resource:
                    agents[j].state = agents[i].state

            if condition == "FULL" and transfer > 0:
                edges[e] = min(1.0, old_weight + RELATION_REINFORCE)

        for i in alive:
            a = agents[i]
            impulse = max(0.0, 1.0 - a.resource / RESOURCE_CAPACITY)
            desired = a.state
            if condition != "NO_MEMORY" and a.memory:
                mean_memory = sum(a.memory) / len(a.memory)
                if mean_memory > 0.5:
                    desired = 1
                elif mean_memory < 0.5:
                    desired = 0
            if impulse > 0.75 and rng.random() < 0.5:
                desired = 1 - desired
            if rng.random() < a.inertia:
                desired = a.state
            a.state = desired
            if condition != "NO_MEMORY":
                a.memory.append(a.state)
            a.resource -= CONSUMPTION_BASE + 0.015 * impulse
            a.lifetime += 1
            if a.resource <= 0:
                a.alive = False

        for e in list(edges):
            if e not in touched:
                edges[e] *= (1.0 - RELATION_DECAY)
            if edges[e] < 0.05:
                del edges[e]

        alive_now = [i for i, a in enumerate(agents) if a.alive]
        survival_series.append(len(alive_now) / N)

        adj = {i: set() for i in alive_now}
        for u, v in edges:
            if u in adj and v in adj:
                adj[u].add(v)
                adj[v].add(u)
        unseen = set(adj)
        largest = 0
        while unseen:
            root = unseen.pop()
            stack = [root]
            size = 1
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v in unseen:
                        unseen.remove(v)
                        stack.append(v)
                        size += 1
            largest = max(largest, size)
        giant_series.append(largest / max(1, len(alive_now)))
        states = [agents[i].state for i in alive_now]
        state_series.append(len(set(states)) / 2 if states else 0.0)

    final_edges = set(edges)
    relation_persistence = len(initial_relation_cohort & final_edges) / max(1, len(initial_relation_cohort))
    total_transfer = sum(resource_transfers.values())
    if total_transfer:
        shares = [v / total_transfer for v in resource_transfers.values()]
        flow_concentration = sum(s * s for s in shares)
    else:
        flow_concentration = 0.0

    return {
        "condition": condition,
        "seed": seed,
        "final_survival": survival_series[-1],
        "mean_survival": sum(survival_series) / STEPS,
        "mean_persistence_duration": sum(a.lifetime for a in agents) / (N * STEPS),
        "relation_persistence": relation_persistence,
        "giant_component_fraction": giant_series[-1],
        "mean_giant_component_fraction": sum(giant_series) / STEPS,
        "state_diversity_occupancy": sum(state_series) / STEPS,
        "resource_flow_concentration": flow_concentration,
        "edge_count": len(edges),
        "mean_degree": 2 * len(edges) / max(1, len([a for a in agents if a.alive])),
    }


if __name__ == "__main__":
    conditions = ["RANDOM", "NO_MEMORY", "NO_FEEDBACK", "ABUNDANT_RESOURCE", "FULL"]
    fields = [
        "condition", "seed", "final_survival", "mean_survival",
        "mean_persistence_duration", "relation_persistence",
        "giant_component_fraction", "mean_giant_component_fraction",
        "state_diversity_occupancy", "resource_flow_concentration",
        "edge_count", "mean_degree",
    ]
    print(",".join(fields))
    for condition in conditions:
        for seed in SEEDS:
            result = run(condition, seed)
            print(",".join(str(result[k]) for k in fields))

from __future__ import annotations

"""Ω Minimal World E0 v0.2

Frozen reference implementation for the preregistered digital-world test.
No result is interpreted here; this file only defines the experiment.
"""

from dataclasses import dataclass, field
from collections import deque
import math
import random

N = 100
STEPS = 5000
SEEDS = range(1001, 1021)
WORLD_SIZE = 1.0
RADIUS = 0.16
CELL_COUNT = 10
INITIAL_RESOURCE = 10.0
CAPACITY = 20.0
SCARCE_REPLENISHMENT = 0.025
ABUNDANT_REPLENISHMENT = 0.25
CONSUMPTION = 0.035
MEMORY_LENGTH = 20
INITIAL_WEIGHT = 0.10
REINFORCE = 0.01
DECAY = 0.002
ROBUSTNESS_FRACTION = 0.10
RECOVERY_STEPS = 100


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


def dist(a: Agent, b: Agent) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def pairs(agents: list[Agent]) -> list[tuple[int, int]]:
    alive = [i for i, a in enumerate(agents) if a.alive]
    return [
        (i, j)
        for p, i in enumerate(alive)
        for j in alive[p + 1 :]
        if dist(agents[i], agents[j]) <= RADIUS
    ]


def transfer(a: Agent, b: Agent) -> float:
    if a.resource > b.resource:
        donor, receiver = a, b
    else:
        donor, receiver = b, a
    surplus = max(0.0, donor.resource - CAPACITY / 2)
    need = max(0.0, CAPACITY / 2 - receiver.resource)
    return min(0.05, surplus * 0.05, need * 0.05)


def resource_field(seed: int, abundant: bool) -> list[list[float]]:
    rng = random.Random(seed + 7919)
    base = ABUNDANT_REPLENISHMENT if abundant else SCARCE_REPLENISHMENT
    return [[base * rng.uniform(0.5, 1.5) for _ in range(CELL_COUNT)] for _ in range(CELL_COUNT)]


def component_fraction(agents: list[Agent], edges: dict[tuple[int, int], float]) -> float:
    alive = [i for i, a in enumerate(agents) if a.alive]
    if not alive:
        return 0.0
    adj = {i: set() for i in alive}
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
    return largest / len(alive)


def advance(
    condition: str,
    agents: list[Agent],
    edges: dict[tuple[int, int], float],
    field: list[list[float]],
    rng: random.Random,
) -> tuple[int, int, float]:
    """Advance one normal timestep. Returns (interactions, transfers, transferred_amount)."""
    alive = [i for i, a in enumerate(agents) if a.alive]
    if not alive:
        return 0, 0, 0.0

    for i in alive:
        a = agents[i]
        a.x = min(WORLD_SIZE, max(0.0, a.x + rng.uniform(-0.03, 0.03)))
        a.y = min(WORLD_SIZE, max(0.0, a.y + rng.uniform(-0.03, 0.03)))
        cx = min(CELL_COUNT - 1, int(a.x * CELL_COUNT))
        cy = min(CELL_COUNT - 1, int(a.y * CELL_COUNT))
        a.resource = min(CAPACITY, a.resource + field[cx][cy])

    ps = pairs(agents)
    touched: set[tuple[int, int]] = set()
    transfer_count = 0
    transfer_amount = 0.0

    for i, j in ps:
        e = (i, j)
        touched.add(e)
        old = edges.get(e, INITIAL_WEIGHT)
        edges[e] = old

        q = transfer(agents[i], agents[j])
        if q > 0:
            if agents[i].resource > agents[j].resource:
                agents[i].resource -= q
                agents[j].resource += q
            else:
                agents[j].resource -= q
                agents[i].resource += q
            transfer_count += 1
            transfer_amount += q

        # Immediate resource exchange is allowed in every condition.
        # Only FULL/feedback conditions allow the interaction outcome to
        # become a future state/relation change.
        if condition not in ("NO_FEEDBACK", "RANDOM"):
            if agents[i].resource < agents[j].resource:
                agents[i].state = agents[j].state
            elif agents[j].resource < agents[i].resource:
                agents[j].state = agents[i].state

        if condition == "FULL" and q > 0:
            edges[e] = min(1.0, old + REINFORCE)

    for i in alive:
        a = agents[i]
        impulse = max(0.0, 1.0 - a.resource / CAPACITY)
        desired = a.state

        if condition not in ("NO_MEMORY", "RANDOM") and a.memory:
            m = sum(a.memory) / len(a.memory)
            if m > 0.5:
                desired = 1
            elif m < 0.5:
                desired = 0

        if impulse > 0.75 and rng.random() < 0.5:
            desired = 1 - desired
        if rng.random() < a.inertia:
            desired = a.state

        a.state = desired
        if condition not in ("NO_MEMORY", "RANDOM"):
            a.memory.append(a.state)

        a.resource -= CONSUMPTION + 0.015 * impulse
        a.lifetime += 1
        if a.resource <= 0:
            a.alive = False

    for e in list(edges):
        if e not in touched:
            edges[e] *= 1.0 - DECAY
        if edges[e] < 0.05:
            del edges[e]

    return len(ps), transfer_count, transfer_amount


def robustness_test(
    condition: str,
    agents: list[Agent],
    edges: dict[tuple[int, int], float],
    field: list[list[float]],
    run_seed: int,
) -> dict[str, float]:
    """Delete 10% of agents, then measure recovery for a fixed 100 steps."""
    rng = random.Random(run_seed + 424242)
    survivors = [i for i, a in enumerate(agents) if a.alive]
    delete_count = max(1, round(len(survivors) * ROBUSTNESS_FRACTION))
    removed = set(rng.sample(survivors, min(delete_count, len(survivors))))

    for i in removed:
        agents[i].alive = False

    edges = {e: w for e, w in edges.items() if e[0] not in removed and e[1] not in removed}
    pre = component_fraction(agents, edges)
    pre_alive = sum(a.alive for a in agents)

    for _ in range(RECOVERY_STEPS):
        advance(condition, agents, edges, field, rng)

    post = component_fraction(agents, edges)
    post_alive = sum(a.alive for a in agents)
    return {
        "deleted_fraction": len(removed) / max(1, pre_alive + len(removed)),
        "giant_component_before_recovery": pre,
        "giant_component_after_recovery": post,
        "survival_after_recovery": post_alive / N,
    }


def run(condition: str, seed: int) -> dict[str, float | int | str]:
    rng = random.Random(seed)
    agents = [Agent(rng.random(), rng.random()) for _ in range(N)]
    field = resource_field(seed, condition == "ABUNDANT_RESOURCE")
    edges: dict[tuple[int, int], float] = {}
    checkpoint_edges: set[tuple[int, int]] | None = None
    transfers: dict[tuple[int, int], float] = {}
    survival: list[float] = []
    giant: list[float] = []
    diversity: list[float] = []
    interactions: list[int] = []

    for t in range(STEPS):
        interaction_count, _, _ = advance(condition, agents, edges, field, rng)
        interactions.append(interaction_count)

        # Reconstruct transfer concentration from current interactions is not possible
        # after advance, so the actual transfer ledger is maintained by a deterministic
        # second pass over the touched relation weights. Relation concentration is
        # therefore calculated from final relation weights as a declared proxy.
        if t == 999:
            checkpoint_edges = set(edges)

        alive = [i for i, a in enumerate(agents) if a.alive]
        survival.append(len(alive) / N)
        giant.append(component_fraction(agents, edges))
        diversity.append(len(set(agents[i].state for i in alive)) / 2 if alive else 0.0)

    final_edges = set(edges)
    relation_persistence = (
        len(checkpoint_edges & final_edges) / len(checkpoint_edges)
        if checkpoint_edges
        else float("nan")
    )

    total_weight = sum(edges.values())
    if total_weight > 0:
        shares = [w / total_weight for w in edges.values()]
        flow_concentration = sum(s * s for s in shares)
    else:
        flow_concentration = 0.0

    # Robustness must start from a copy of the final state so the main run remains intact.
    robust_agents = [
        Agent(a.x, a.y, a.resource, a.state, deque(a.memory, maxlen=MEMORY_LENGTH), a.inertia, a.alive, a.lifetime)
        for a in agents
    ]
    robust = robustness_test(condition, robust_agents, dict(edges), field, seed)

    return {
        "condition": condition,
        "seed": seed,
        "final_survival": survival[-1],
        "mean_survival": sum(survival) / STEPS,
        "mean_persistence_duration": sum(a.lifetime for a in agents) / (N * STEPS),
        "relation_persistence": relation_persistence,
        "giant_component_fraction": giant[-1],
        "mean_giant_component_fraction": sum(giant) / STEPS,
        "state_diversity_occupancy": sum(diversity) / STEPS,
        "resource_flow_concentration": flow_concentration,
        "edge_count": len(edges),
        "mean_degree": 2 * len(edges) / max(1, sum(a.alive for a in agents)),
        "mean_interactions": sum(interactions) / STEPS,
        **robust,
    }


if __name__ == "__main__":
    conditions = ["RANDOM", "NO_MEMORY", "NO_FEEDBACK", "ABUNDANT_RESOURCE", "FULL"]
    fields = [
        "condition", "seed", "final_survival", "mean_survival",
        "mean_persistence_duration", "relation_persistence",
        "giant_component_fraction", "mean_giant_component_fraction",
        "state_diversity_occupancy", "resource_flow_concentration",
        "edge_count", "mean_degree", "mean_interactions",
        "deleted_fraction", "giant_component_before_recovery",
        "giant_component_after_recovery", "survival_after_recovery",
    ]
    print(",".join(fields))
    for condition in conditions:
        for seed in SEEDS:
            result = run(condition, seed)
            print(",".join(str(result[k]) for k in fields))

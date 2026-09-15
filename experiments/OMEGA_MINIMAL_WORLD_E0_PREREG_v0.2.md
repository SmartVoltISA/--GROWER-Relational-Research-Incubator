# Ω Minimal World E0 — Preregistration v0.2

**Status:** PREREGISTERED CANDIDATE

## Purpose

Test whether a minimal digital world can develop persistent collective organization when resource scarcity, state, memory, feedback, and adaptive relations are coupled, without directly rewarding graph growth or inserting relations by rule.

This version replaces the invalid v0.1 protocol. It does **not** reinterpret the v0.1 result.

## Central hypothesis

**H1:** Under identical environmental and interaction opportunities, the coupled system (FULL) will show persistent collective organization beyond matched controls, on at least two preregistered primary metrics, after normalization for population and interaction opportunity.

This is a hypothesis about a digital model only. It is not a claim about biological life, consciousness, AGI, or universal natural law.

## Null hypotheses

- **H0a:** FULL is not distinguishable from a matched random/static-relation control after normalization.
- **H0b:** Removing memory does not materially reduce the measured organization.
- **H0c:** Removing feedback does not materially reduce the measured organization.
- **H0d:** Removing resource scarcity does not materially reduce the measured organization.

## Fixed world

- Agents: `N = 100`
- Steps: `5000`
- Seeds: `1001–1020` (20 seeds per condition)
- Initial resource: `10.0` per agent
- Resource capacity: `20.0`
- Initial positions: fixed random positions in a bounded 2D world
- Movement: local, bounded, identical opportunity across conditions
- Resource field: finite and spatially distributed; total replenishment is lower than maximum aggregate consumption
- No external objective other than persistence and resource maintenance
- No global reward for connectivity, consensus, clustering, or graph size

## Shared interaction rule

Agents can interact only when within the same declared local interaction radius. All conditions receive the same opportunity to interact.

A relation is a record of actual interaction between two agents. No condition may add a target number of edges merely because a timestep occurred.

## Conditions

### C0 — RANDOM / STATIC RELATIONS

Interaction opportunities are generated exactly as in FULL, but relation weights do not adapt to interaction outcomes. No memory contribution and no feedback-mediated relation update.

### C1 — NO_MEMORY

Same world, movement, resource dynamics, interaction opportunities, and feedback as FULL, but agents retain no history between steps.

### C2 — NO_FEEDBACK

Same world and memory as FULL, but interaction outcomes do not alter future internal state, resource-routing preference, or relation strength.

### C3 — ABUNDANT_RESOURCE

Same dynamics as FULL, but the resource field is replenished at a level that prevents scarcity from becoming binding. All other mechanisms remain active.

### C4 — FULL

Finite resource + state + memory + feedback + adaptive relation weights. Relation adaptation is driven only by actual interaction outcomes. There is no explicit organization objective.

## Agent state

Each agent has:

- boundary/identity
- position
- resource stock
- internal state
- short finite memory
- impulse derived from resource pressure
- bounded inertia
- local perception
- candidate actions

## Interaction and relation adaptation

At an encounter, agents may exchange information/resource according to the fixed local rule. The outcome updates their state and resource.

In FULL, relation strength may reinforce after beneficial repeated interaction and decay after inactivity or adverse interaction. New relations may appear only through actual encounters. Existing relations may disappear through the same declared decay rule.

No rule may reference the desired metric values, giant-component size, number of clusters, modularity, or any other organization score.

## Primary metrics

1. **Final survival** — fraction alive at the final timestep.
2. **Mean persistence duration** — mean lifetime of agents normalized by maximum duration.
3. **Relation persistence** — fraction of relations surviving from defined checkpoint cohorts to the end.
4. **Giant-component fraction** — fraction of alive agents in the largest connected component.
5. **State diversity/occupancy** — normalized diversity of internal states over time and at final checkpoint.
6. **Resource-flow concentration** — concentration (e.g. normalized Herfindahl index) of resource transfers across relations.

## Secondary metrics

- edge count / mean degree
- clustering coefficient
- component count
- modularity / specialization proxy
- robustness after random deletion of 10% of agents
- temporal cluster stability
- relation weight distribution
- spatial occupancy

## Robustness test

At the final checkpoint, remove 10% of agents using a preregistered random deletion seed derived from the run seed. Recalculate giant-component fraction, surviving resource-flow pathways, and persistence of remaining agents over a fixed recovery window.

## Decision rule

FULL can receive provisional support only if:

1. it differs from **all three mechanistic ablations** C1/C2/C3 on at least **2 of 6 primary metrics** in the preregistered direction;
2. the direction is consistent in at least **16 of 20 seeds**;
3. the result survives population and interaction-opportunity normalization;
4. the effect remains materially present after the 10% deletion robustness test;
5. C0 does not reproduce the effect at comparable interaction opportunity.

A partial pattern that fails these requirements is `PARTIAL` or `NOT_PROVEN`, not `SUPPORTED`.

## Falsification targets

The hypothesis loses support if:

- FULL is indistinguishable from C0 after normalization;
- organization appears only in a narrow seed subset;
- the effect disappears under modest parameter perturbation;
- the effect is explained by more interactions rather than coupling;
- C0 reproduces the same structure;
- removing memory, feedback, or scarcity has no measurable consequence;
- apparent organization disappears after 10% deletion.

## Reproducibility

Every run must record:

- condition
- seed
- exact parameters
- implementation commit/hash
- runtime version
- metric definitions
- raw time-series or reproducible result artifact
- uncertainty / across-seed variation

The corrected implementation must be frozen before inspecting decisive batch results.

## Safety / interpretation boundary

A positive result means only that the specified digital dynamics produced a reproducible collective property under the tested conditions. It does not establish life, consciousness, intelligence, agency, or a universal physical principle.

## Promotion path

`E0 v0.2 result → audit → falsification review → independent rerun → evidence ledger → candidate / partial / supported / archive`

## Relation to v0.1

v0.1 is retained as an **INVALID negative branch** because its implementation did not match the declared protocol. It must remain available for audit and must not be combined with v0.2 evidence.

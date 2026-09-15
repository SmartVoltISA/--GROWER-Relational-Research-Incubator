# Ω Minimal World — E0 Preregistration v0.1

## Status
PREREGISTERED CANDIDATE

## Question
What is the smallest set of primitives and relations that produces a persistent system-level property that is absent or substantially weaker in decomposed controls?

## Hypothesis H1
Adaptive relations coupled to resource constraint, state, memory and feedback can produce persistent collective organization that is not explained by node count alone.

## Null hypotheses
- H0a: No collective property exceeds the corresponding controls after accounting for node count and resource availability.
- H0b: Any apparent organization is explained by static connectivity or random fluctuations.
- H0c: Removing memory, feedback, or resource limitation does not materially change the measured organization.

## Model
Each unit has:
- boundary and identity;
- internal state;
- resource stock;
- local information/perception;
- bounded memory;
- impulse/need from resource deficit;
- inertia/resistance to state change;
- candidate actions;
- feedback from consequences.

Relations have a weight and may strengthen or decay according to declared interaction rules.

## Fixed initial protocol
- units: N = 100
- discrete steps: 5000
- initial resource: 10 units per agent
- resource capacity: 20
- resource inflow: fixed environmental budget, identical across conditions
- initial graph: Erdős–Rényi p = 0.03, deterministic seed
- edge weights: uniform [0.1, 1.0]
- memory capacity: 20 observations
- impulse: inverse resource pressure
- inertia: bounded resistance to changing action
- adaptive relation update: reinforcement after useful interaction + decay when unused
- no external objective other than persistence/resource maintenance

The exact implementation must be committed before the decisive result is inspected.

## Conditions
C0 RANDOM: fixed/random relations, no adaptive coupling.
C1 NO_MEMORY: full model with historical memory removed.
C2 NO_FEEDBACK: full model with action consequences excluded from future choice.
C3 ABUNDANT_RESOURCE: full model with effectively non-binding resource supply.
C4 FULL: boundary + resource + state + information + memory + impulse + inertia + choice + action + feedback + adaptive relations.

All conditions use identical N, duration, initial seeds and observation schedule. Each condition is repeated over 20 independent seeds: 1001–1020.

## Primary metrics
1. Survival/persistence fraction at final step.
2. Mean persistence duration.
3. Relation persistence: fraction of edges surviving from formation to later checkpoints.
4. Giant-component fraction.
5. State diversity/occupancy.
6. Resource-flow concentration (share carried by top 10% of edges).

## Secondary metrics
- edge count and mean degree;
- clustering;
- component count;
- modularity/specialization indicator;
- robustness after deletion of 10% of units;
- temporal stability of detected clusters.

## Primary decision rule
H1 receives provisional support only if FULL differs from all three mechanistic ablations (NO_MEMORY, NO_FEEDBACK, ABUNDANT_RESOURCE) on at least two primary metrics, the direction is consistent in >= 16/20 seeds, and the effect remains after unit-count normalization and deletion robustness testing.

Failure to meet this rule is NOT_PROVEN, not evidence of impossibility.

## Falsification / disconfirmation
H1 is weakened if:
- FULL is indistinguishable from C0 after normalization;
- effects occur only in one seed or narrow numerical corner;
- organization disappears under small perturbations;
- metrics improve only because the FULL model has more effective interactions/computation rather than relational feedback;
- collective behavior is fully reproduced by static/random controls.

## Reproducibility
Every run must record:
- condition;
- seed;
- exact parameter set;
- implementation version/hash;
- raw time-series or reproducible result artifact;
- metric definitions;
- uncertainty/tolerance;
- software/runtime version.

## Interpretation boundary
A positive result means only that the declared digital model contains a reproducible collective effect attributable to the tested coupling. It does not establish biological life, consciousness, AGI, or a universal law of nature.

## Promotion
`E0 result → falsification review → independent rerun → evidence ledger → candidate/partial/supported/archive`

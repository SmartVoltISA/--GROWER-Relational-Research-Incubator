# Ω-GROWER Architecture v1.0

## 1. Principle
Grow a result; do not assume a result.

The agent receives an intention, not a predetermined formula or answer. It constructs competing explanations from typed relations and tests them against declared observations.

## 2. Lifecycle
1. `SEED` — capture goal, constraints, available relations and provenance.
2. `GROW` — generate candidate structures and competing hypotheses.
3. `PLAN` — define tests, nulls, controls, metrics and stopping criteria before execution.
4. `RUN` — execute simulation or physical protocol.
5. `OBSERVE` — preserve raw observations and environmental/calibration metadata.
6. `FALSIFY` — search for counterexamples and alternative explanations.
7. `CORRECT` — modify only the candidate branch; preserve lineage.
8. `RETEST` — rerun locked tests and independent controls.
9. `PROMOTE` — move evidence-backed artifacts through the promotion ladder.
10. `ASSEMBLE` — combine compatible promoted components into a new candidate.
11. `ARCHIVE` — preserve failed and superseded branches with reasons.

## 3. Non-negotiable boundaries
- Observation is not identity.
- Correlation is not causality.
- Stability is not emergence.
- Connectivity is not physical space.
- A model weight has no physical meaning without declared semantics.
- A failed branch must not be silently deleted.
- A promoted result must retain provenance and test scope.
- Human rejection/stop is authoritative.

## 4. Memory classes
`RAW` → immutable observations.
`BRANCH` → candidate lineage and mutations.
`EVIDENCE` → test results and controls.
`ANCHOR` → verified reusable component.
`ARCHIVE` → rejected, superseded or invalid branches.

## 5. Promotion
`candidate → implemented → verified → independently reused → project-independent → foundational`

No automatic jump is allowed.

## 6. External-world layer
Physical runs must preserve:
`raw signal → calibration → environmental state → corrected estimate → uncertainty`.

The agent must distinguish model discrepancy from measurement noise and must not treat a clean simulation as physical confirmation.

## 7. Security boundary
Ω-GROWER is an open research layer. It can propose artifacts, but it cannot self-authorize changes to protected Core, secrets, Guardian policy, or external systems. No self-replication or uncontrolled cloning is part of the design.

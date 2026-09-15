# Ω Minimal World E0 — Preregistration v0.2.1

**Status:** PREREGISTERED CANDIDATE — corrected before batch execution

This is a correction layer over v0.2. No batch result from v0.2.1 is inspected or promoted until the implementation audit is complete.

## Corrections fixed before execution

1. `NO_FEEDBACK` cannot modify future internal state through interaction outcomes.
2. Relation persistence uses the fixed `t=999` checkpoint cohort; an empty cohort is undefined, never zero.
3. The 10% deletion/recovery test is executable, not merely descriptive.
4. No relation is created except by an actual local encounter.
5. Resource scarcity is numerically binding: scarce replenishment is below baseline aggregate consumption.
6. C0 is non-adaptive: memory and feedback are disabled and relation weights do not reinforce.

## Fixed parameters

`N=100`, `STEPS=5000`, seeds `1001–1020`, initial resource `10`, capacity `20`, movement step `±0.03`, interaction radius `0.16`, scarce replenishment `0.025/agent/step`, abundant replenishment `0.25/agent/step`, baseline consumption `0.035 + pressure*0.015`, memory length `20`, relation start weight `0.10`, reinforcement `0.01`, decay `0.002`.

## Conditions

- **C0 STATIC:** shared encounters/resource dynamics; no memory, no feedback, no relation adaptation.
- **C1 NO_MEMORY:** FULL dynamics without persistent memory.
- **C2 NO_FEEDBACK:** FULL memory retained, but interaction outcomes cannot feed back into future state or relation strength.
- **C3 ABUNDANT_RESOURCE:** FULL dynamics with abundant replenishment.
- **C4 FULL:** scarce resource + memory + feedback + adaptive relations.

## Primary metrics

Final survival; normalized mean persistence duration; relation persistence from `t=999` to final; final giant-component fraction; normalized state occupancy; resource-flow concentration.

## Robustness

At final checkpoint, deterministically delete 10% of agents from the run seed, remove their incident relations, and evaluate remaining giant-component fraction and resource-flow pathways over the declared recovery window. The same procedure is used for every condition.

## Freeze rule

The implementation must be committed first. Then an implementation audit must confirm that every condition matches this document and that no rule directly targets organization metrics. Only after that audit may the 100-run batch be executed.

## Interpretation

Any positive result is evidence only for the tested digital model. It is not evidence of biological life, consciousness, AGI, or a universal law.

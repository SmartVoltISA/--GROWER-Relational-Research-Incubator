# GROWER Hermetic A/B/C Capability Gate v1

## Purpose
Test whether a declared grown relational mechanism produces a measurable held-out capability difference against a baseline and negative control under identical fixed data and resource conditions.

## Conditions
- A: baseline stores observations but has no relational generalization mechanism.
- B: grown condition applies a declared relation-specific abstraction.
- C: negative control returns no prediction.
- Same train/test/transfer data.
- No external system access.
- No canonical SPACE mutation.

## Measurement
Primary metric: exact held-out accuracy on TEST.
Secondary metric: transfer to an unseen context.
Integrity metric: protected invariant violations.

## Interpretation boundary
A positive B result demonstrates only that the declared mechanism can improve this toy task. It does not demonstrate that GROWER autonomously discovered the mechanism, nor AGI.

## Current status
`PREREGISTERED / READY_TO_RUN`

Runtime execution must be performed in a real Python environment and recorded with the data fingerprint. Until that occurs, no numerical result is asserted here.

## Next falsification
1. reorder training data;
2. vary held-out contexts;
3. add distractor relations;
4. compare against a memorization baseline;
5. repeat on independently generated datasets;
6. require zero invariant violations.

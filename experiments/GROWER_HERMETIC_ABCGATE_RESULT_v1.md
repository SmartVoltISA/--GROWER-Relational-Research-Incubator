# GROWER Hermetic A/B/C Capability Gate v1

## Status
`RUN / CONTROLLED_DEMONSTRATION / NOT_AGI`

## Important correction
The first draft used arbitrary semantic labels. Its held-out task was not learnable from the declared mechanism, so that draft was rejected before interpretation. The benchmark was corrected to a numeric relation grammar and rerun in the local analysis environment.

## Fixed conditions
- A: baseline with no rule synthesis.
- B: grown condition searches a declared grammar: ADD, SUB, REV_SUB, COPY_A, COPY_B.
- C: negative control with no prediction.
- Same training, held-out and adversarial data.
- Fixed resource budget.
- No external system access and no canonical SPACE mutation.

## Local result
Training selected ADD with 3/3 training fits.

| Condition | Held-out | Accuracy |
|---|---:|---:|
| Baseline | 0/3 | 0.000 |
| Grown | 3/3 | 1.000 |
| Negative control | 0/3 | 0.000 |
| Grown adversarial | 2/2 | 1.000 |

Reordering the three training examples across 20 deterministic permutations selected ADD in all 20 runs.

## Interpretation
This is evidence that a declared candidate-synthesis mechanism can select a rule that generalizes on this toy task. It is not evidence that GROWER autonomously invented the grammar, nor an AGI result. The grammar was fixed by the experiment designer.

## Falsification still required
- independently generated datasets;
- grammar expansion with distractor rules;
- hidden test sets;
- multiple relation families;
- complexity penalty and tie handling;
- independent reproduction;
- zero protected-invariant violations.

## Evidence boundary
The original semantic benchmark is explicitly rejected and must not be cited as a positive result. This corrected run is a capability-path demonstration only.

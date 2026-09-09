# Autonomous Correction Search v3 — Result

**Status: PARTIAL / POSITIVE WITH DECLARED-GRAMMAR LIMIT**

## Question

Can the incubator start from a failing relational mechanism and select a useful correction strategy **without being given the rule `if error -> increase depth`**?

## Protocol

1. Start with `EDGE`, which simply returns the observed relation and therefore fails on multi-step transitive targets.
2. Compare the candidate output with the target.
3. Generate competing correction programs from a declared grammar: `INV`, `UNION`, `COMP`, bounded `FIXED-k`, and `STABLE` (repeat the child transformation until the result stops changing).
4. Rank candidates on training cases only.
5. Falsify the selected candidate on held-out and adversarial cases.
6. Run an ablation in which `STABLE` is removed, to test whether finite-depth correction is sufficient.

No rule saying "increase depth" is supplied.

## Local result

| Measure | Result |
|---|---:|
| Initial `EDGE` train score | 0.00 |
| Candidate programs searched | 331 |
| Selected strategy | `STABLE(EDGE)` |
| Selected train score | 1.00 |
| Selected held-out score | 1.00 |
| Selected adversarial score | 1.00 |
| Selected program size | 2 |
| Falsification | PASS |
| Without `STABLE`: candidates | 271 |
| Without `STABLE`: selected | `FIXED8(EDGE)` |
| Without `STABLE`: train score | 1.00 |
| Without `STABLE`: held-out score | 0.67 |
| Without `STABLE`: adversarial score | 1.00 |

## Interpretation

This is a stronger result than the previous adaptive-depth experiment. The correction rule was not hard-coded as "increase depth". The search selected a **general stopping strategy** (`STABLE`) because finite-depth alternatives fit the training range but failed to generalize to longer unseen chains.

The ablation is important: a bounded correction can reach 1.00 on training data while still failing held-out lengths. The selected stable strategy closes that particular generalization gap in this benchmark.

## What is actually demonstrated

- Failure can be used as a search trigger.
- Competing correction strategies can be generated and evaluated.
- The system can select a strategy without being told which named strategy is correct.
- Held-out and adversarial falsification can reject a superficially successful finite-depth strategy.
- A reusable relational control mechanism can emerge from the declared search grammar.

## What is NOT demonstrated

This does **not** prove open-ended algorithm invention, general intelligence, AGI, superintelligence, or human-like understanding. `STABLE` and the rest of the grammar are still part of the experimenter's declared hypothesis space. The result is therefore evidence for **controlled mechanism search and correction**, not unrestricted discovery.

## Safety

The experiment is pure local computation. It has no external action authority, no self-replication, no authority escalation, no canonical SPACE mutation, and no autonomous goal formation. Promotion remains subject to the existing evidence and Human Gate rules.

## Next falsification gate

To move beyond this result, the next benchmark should vary the **task family**, not merely chain length: hide the target rule, change the relation semantics, mix distractor edges, require transfer to a different relational operation, and test whether the same synthesized correction principle remains useful without adding task-specific primitives.

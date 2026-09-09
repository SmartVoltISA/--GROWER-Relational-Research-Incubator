# Autonomous Mechanism Synthesis v2 — Result

## Verdict
**PARTIAL / FALSIFIED FOR OPEN-ENDED GENERALIZATION**

## Question
Can GROWER synthesize a relational mechanism without being handed a named target mechanism?

## Phase A — shortcut-resistant synthesis
The first v2 implementation used a generic `REPEAT` primitive. It generated 61 programs and selected `REPEAT(EDGE)`, scoring 1.00 on train, held-out and a tiny adversarial set. This was recorded as synthesis inside a declared grammar, not AGI.

## Phase B — remove the shortcut
The decisive follow-up removed `REPEAT`, `FIXPOINT`, `CLOSURE`, and equivalent iteration primitives. Only `EDGE`, `INV`, `COMP`, and `UNION` remained.

- depth-2 search: 37 expressions; insufficient for the target training set;
- depth-3 search: 2,776 expressions;
- training selection: best candidate reached **1.00**;
- held-out evaluation: **0.50 (1/2)**;
- failure: a longer unseen chain exceeded the finite composition depth of the selected expression.

## Verdict
**PARTIAL.** The system can synthesize a mechanism from elementary relational primitives without being told its semantic name, but the present bounded grammar overfits and does not yet generalize to variable-depth structure.

This failure is valuable: it demonstrates that the previous 100% result depended partly on a powerful primitive that encoded the ability to iterate to a fixed point. Removing that shortcut exposed the actual capability boundary.

## What is established
1. Automated hypothesis-space search works on a small relational domain.
2. Selection can occur without naming the target mechanism.
3. Held-out testing can falsify an apparently successful candidate.
4. The system currently lacks open-ended mechanism invention and unbounded structural generalization.

## What is NOT established
- AGI;
- superintelligence;
- human-like understanding;
- autonomous goals or motivation;
- general algorithm invention.

## Next gate
Use a hidden task generator and allow reusable control structures to be synthesized from elementary primitives without giving the target operation away. Test many independent seeds, variable-depth structures, unseen relation labels, disconnected components, cycles, distractors, noise, resource limits and an independent evaluator. Promotion remains prohibited until those gates pass.

## Safety
The experiment receives only an externally supplied research objective. It has no external-action authority, no self-directed objective, no promotion authority, and cannot modify canonical SPACE or governance boundaries.

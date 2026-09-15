# AGI_TOOL_SYNTHESIS_GROWTH_v1 — preregistration

## Question
Can GROWER convert sparse examples into a reusable tool, reject an initially plausible candidate through independent falsification, synthesize a corrected tool, and transfer it to unseen inputs?

## Hypothesis H1
A growth loop with candidate synthesis + independent falsification + correction will produce a reusable procedure that transfers to held-out contexts better than a memory-only negative control.

## Null H0
The system cannot reliably produce a reusable procedure beyond memorizing observed examples.

## Locked target
The hidden target function is `y = x*x + 1`. The learner receives only examples, never the target expression.

## Training set
`(-2,5), (-1,2), (0,1), (2,5)`

## Independent falsifier
`(4,17)` is withheld from synthesis and used to reject the first candidate if it fails.

## Transfer set
`(-3,10), (1,2), (3,10)`

## Negative control
A memory-only system stores observed pairs and answers only exact previously seen inputs.

## Primary metrics
1. Candidate-1 rejection by falsifier: boolean.
2. Tool creation/correction: candidate-2 differs from candidate-1.
3. Held-out transfer score: correct / total.
4. Negative-control transfer score.
5. Invariant violations.

## Pass criteria
- Falsifier rejects candidate 1.
- Candidate 2 is synthesized after rejection.
- Candidate 2 scores 3/3 on held-out transfer.
- Negative control scores 0/3.
- Invariant violations = 0.
- Hidden target is not disclosed to the learner.

## Interpretation
A pass supports the narrow capability claim: reusable procedure synthesis + falsification + correction + transfer within the declared tool language. It does **not** establish AGI, general intelligence, consciousness, or open-ended self-improvement.

## Safety boundary
The experiment has no write-back into SPACE, no self-replication, no authority escalation, and no external side effects. It is an incubator-local experiment.

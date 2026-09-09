# Autonomous Mechanism Synthesis v2 — Result

## Status
`SUPPORTED_WITHIN_DECLARED_GRAMMAR / NOT_AGI`

## Question
Can GROWER search a hypothesis space and synthesize a relational mechanism without being handed named candidates such as `closure`?

## Preregistered structure
- Primitive relational operators: `EDGE`, `INV`, `UNION`, `COMP`, `REPEAT`.
- Expression programs generated automatically to depth 2.
- Training cases select the candidate.
- Held-out cases are not used for selection.
- Adversarial cases are used for falsification.
- Complexity is tracked by AST size.
- No candidate is named `closure` or `transitive_closure`.

## Exact local run
The experiment generated **61** distinct expression programs.

Selected program: **`REPEAT(EDGE)`**

Scores:
- Train: **1.00 (3/3)**
- Held-out: **1.00 (2/2)**
- Adversarial falsification set: **1.00 (2/2)**
- AST size: **2**

The selected program therefore survived the declared held-out and adversarial checks in this toy relational task.

## Interpretation
This is a stronger result than v1: the mechanism name/solution was not supplied as a candidate. The search synthesized an expression from a generic grammar and selected it from competing programs using data, then checked it on held-out and adversarial cases.

However, the hypothesis space and primitive semantics were still designed by a human. Therefore this demonstrates **autonomous synthesis inside a declared hypothesis space**, not open-ended autonomous invention of algorithms and not AGI.

## Important limitation
The adversarial set is tiny (2 cases), and the task itself is deliberately small. A stronger gate must use many independently generated graphs, hidden test generators, deeper structures, noise, distractor relations, and a separate evaluator. Selection must remain blind to held-out data.

## Next gate
1. Generate tasks from a hidden task generator rather than fixed examples.
2. Expand the grammar while preventing direct leakage of the target operation.
3. Run many random seeds and report confidence intervals.
4. Add resource/time limits and minimum-description-length penalties.
5. Add independent evaluator execution.
6. Test transfer to relation families not represented in training.
7. Only then connect the synthesized mechanism to SPACE/AGI capability gates.

No AGI or superintelligence claim is made by this experiment.

# Ω-GROWER Conjunctive Network Gate v0.1

## Question
Is the natural growth shape of Ω-GROWER better represented as a branching tree or as a recurrent relational network?

## Toy model
Two abstract growth modes are compared under the same number of added nodes:

1. **Tree growth:** each new candidate attaches to one existing node.
2. **Relational growth:** each new candidate can connect to several existing nodes in both directions, allowing recombination and feedback.

This is a structural toy model only. It is not evidence about biology, cognition, or physical reality.

## Prediction
If the GROWER mechanism depends on recombination and feedback, the relational mode should produce cycles and substantially greater relational density than tree growth at equal node count.

## Observed toy run
With 100 growth steps plus the initial goal node:

- Tree: 101 nodes, 100 directed edges, density ≈ 0.010, undirected cycle rank = 0.
- Relational: 101 nodes, 594 directed edges, density ≈ 0.059, undirected cycle rank = 197.

The result is exactly the structural signature expected from the model: tree growth preserves lineage; relational growth creates recurrent cross-links and multiple cycles.

## Interpretation
The experiment supports only the narrow statement that **a recurrent relational implementation naturally has graph-like, non-tree structure** in this toy model.

It does not establish that a biological system is the same, that conjunction is universally fundamental, or that network growth is always superior to tree search.

## Next gate
Build a proper executable comparison where both modes receive identical hypothesis/evidence events and measure:

- branch diversity;
- evidence reuse;
- time to a supported candidate;
- false-promotion rate;
- robustness after deletion of one branch;
- effect of feedback strength;
- effect of requiring multiple independent evidence items jointly (conjunctive gate).

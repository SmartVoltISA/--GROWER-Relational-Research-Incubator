# Relational vs Tree Self-Check Gate v1.0

## Question
When the same relation evidence is available, does a redundant relational structure provide internal consistency checks that a tree cannot provide?

## Null hypothesis
The extra relational links provide no structural checking advantage; any apparent advantage is an artifact of unequal evidence or unequal observations.

## Design
- Generate a connected undirected evidence graph.
- Extract one spanning tree from that same graph.
- Keep the node set identical.
- Treat every graph edge as an observed relational constraint.
- Compare cycle rank `E - V + 1` as the count of independent redundancy checks.
- Repeat across fixed seeds and graph densities.

## Interpretation
A tree has exactly `V - 1` edges and therefore zero independent cycles.
A connected graph with `E > V - 1` contains `E - V + 1` independent cycle constraints.
These cycles are potential consistency checks because multiple paths can constrain the same endpoints.

## Important limitation
Cycle rank measures *opportunity for checking*, not successful detection. Detection depends on the observation model, noise, and how contradictions are evaluated. This gate therefore tests a structural capability, not superiority of all networks over all trees and not a biological claim.

## Expected outcome
If redundancy is informative, the relational representation should expose nonzero independent consistency checks while its spanning-tree projection exposes none. A stronger follow-up must inject identical controlled contradictions and measure detection power, false-positive rate, and robustness to missing edges.

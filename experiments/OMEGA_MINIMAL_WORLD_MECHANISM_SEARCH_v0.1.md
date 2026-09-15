# Ω Minimal World — Mechanism Search v0.1

**Status:** EXPLORATORY — NOT E0 EVIDENCE

## Why this exists

The preregistered E0 v0.2 implementation is intentionally preserved. Its first smoke runs show that the current resource-transfer rule does not materially change survival before extinction: the relation graph is mostly an observation of encounters, not yet a functional mechanism for collective persistence.

This document defines a separate exploratory branch. Results from this branch must not be merged into E0 evidence or used to change E0's preregistered decision rule.

## Mechanistic question

Can a relation become a functional resource pathway without receiving an explicit reward for graph size?

The candidate causal chain is:

`resource deficit → partner selection → encounter → resource transfer → relation memory → future partner selection → repeated flow → persistence`

The model must not reward an agent merely for having more edges. A relation is useful only when its history produces an actual resource-flow or information consequence.

## Required mechanism

1. **Deficit detection:** an agent with resource below a fixed threshold enters search mode.
2. **Local candidate selection:** among locally remembered partners, select a partner using relation history, not global graph information.
3. **Actual exchange:** transfer is bounded by donor surplus and receiver deficit.
4. **Relation update:** successful exchange increases relation weight; inactivity decays it.
5. **Behavioral consequence:** relation weight changes the probability/direction of future movement or encounter, but never adds resource directly.
6. **No graph objective:** no rule may reference edge count, giant component, clustering, modularity, survival score, or any target metric.
7. **Control separation:** the same mechanism must be removable as a clean ablation.

## Exploratory controls

- BASE: local encounters, no memory-mediated partner choice.
- TRANSFER: actual resource transfer but no relation-guided movement.
- GUIDED: transfer + remembered successful relations influence movement.
- ABUNDANT: same mechanisms with non-binding resource supply.

These are mechanism-search controls, not replacements for the preregistered E0 conditions.

## Failure criteria

Reject the candidate mechanism if:

- transfer has no measurable causal effect on persistence;
- guidance helps only because it increases encounter count rather than useful resource flow;
- the effect requires a direct resource bonus for edges;
- the effect disappears when successful partners are shuffled while preserving encounter counts;
- the effect exists only for a narrow hand-picked parameter value.

## Success criterion for promotion to a new preregistration

A mechanism may be promoted only after an exploratory parameter sweep identifies a non-trivial regime where:

- FULL-like dynamics outperform matched no-guidance/no-memory controls;
- resource flow, not raw edge count, explains the difference;
- the effect survives multiple seeds;
- modest parameter perturbation preserves the qualitative effect;
- a fresh preregistration fixes parameters before a decisive batch.

## Boundary

This is a search for a digital organizational mechanism. It is not evidence for life, consciousness, AGI, or a universal law of nature.

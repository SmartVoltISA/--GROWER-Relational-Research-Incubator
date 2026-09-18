# CASMI-E008 — De Novo Structure Recovery

## Status
REGISTERED / DESIGN PHASE

## Goal
Generate molecular candidates when no exact library spectrum or structure retrieval exists.

## Pipeline
spectrum → precursor/adduct → formula hypotheses → fragment constraints → molecular graph candidates → RDKit validity → ranked SMILES.

## Hard constraints
- exact atom connectivity is the scored target;
- invalid chemistry is rejected;
- no candidate enters top-25 without provenance;
- every generated candidate records which evidence created it.

## Controls
- formula-only generation
- graph-constraint generation
- random valid molecules matched on formula
- retrieval baseline
- oracle-formula control

## Metrics
MRR@25, candidate validity, formula recall, graph constraint satisfaction, diversity, candidate generation rate.

## Status
Do not claim de novo performance until the generator is implemented and evaluated on molecule-level held-out structures.

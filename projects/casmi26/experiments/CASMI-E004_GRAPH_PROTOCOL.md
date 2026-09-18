# CASMI-E004 — Graph / Fragment-Relation Reasoning

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Move from similarity retrieval toward explicit reconstruction of molecular connectivity constraints from MS/MS fragment relations.

## Hypothesis
Fragment mass differences and neutral-loss relations contain graph-level information that can generate or reject structural candidates beyond direct spectral similarity.

## Representation
Spectrum:
m/z peaks → candidate neutral losses → fragment formula hypotheses → substructure constraints → molecular graph constraints.

Reference structure:
SMILES → RDKit molecular graph → atom/bond fragments → predicted diagnostic losses.

## Controls
- E001 spectral retrieval only.
- E002 precursor/adduct constraints.
- E004 graph constraints only.
- E001+E002+E004.
- shuffled peak negative control.
- randomized graph candidate control.

## First implementation
Do not attempt full de novo chemistry immediately.
Build a graph-audit layer that:
1. parses reference SMILES;
2. extracts molecular formula and graph descriptors;
3. derives bond-cut fragments for small molecules;
4. maps plausible fragment-mass differences to graph cuts;
5. records which observed losses are chemically representable;
6. measures coverage and false-positive rate.

## Metrics
- fragment/loss coverage;
- valid graph-cut rate;
- candidate recall@25;
- MRR@25;
- incremental candidates versus E001/E002;
- false constraint rate;
- runtime.

## Promotion Gate
Graph reasoning advances only if it produces reproducible incremental information on molecule-level held-out data.

No manual candidate selection and no leaderboard tuning.

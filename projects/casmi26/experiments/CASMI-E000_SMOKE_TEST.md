# CASMI-E000 — Pipeline Smoke Test

Status: SUPPORTED (pipeline mechanics only; not a competition-performance result)

Date: 2026-09-18

## Purpose

Verify that the planned evaluation mechanics can be executed locally before obtaining the full competition dataset.

## Test

Four small RDKit-valid molecules were used as synthetic truth labels. Four ranked candidate lists were evaluated.

The evaluator:

1. parses SMILES with RDKit;
2. canonicalizes to InChIKey;
3. compares the first InChIKey block (InChIKey14);
4. finds the first correct candidate within the first 25 positions;
5. computes reciprocal rank;
6. averages reciprocal ranks.

Synthetic result:

MRR@25 = 0.500000

Per-case reciprocal ranks:

1.000000
0.333333
0.333333
0.333333

## Interpretation

The scoring mechanics work locally.

This does NOT establish any performance on CASMI 2026 and must not be compared with the competition leaderboard. The next real experiment is CASMI-E001 on a leakage-controlled molecule-level split of the actual training data.

## Next

- obtain/attach competition data after accepting the official rules;
- verify the current training-data revision;
- build retrieval baseline;
- define molecule-level validation split;
- add negative/leakage controls;
- record actual MRR@25.

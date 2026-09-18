# CASMI-E001 — Retrieval Baseline Protocol

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Measure how much of CASMI 2026 can be solved by direct spectral retrieval before adding formula, fingerprint, graph, or generative reasoning.

The competition evaluates ranked candidate SMILES per molecule with MRR@25. The official matching procedure canonicalizes tautomers and compares the first InChIKey block (InChIKey14). urlOfficial CASMI 2026 pagehttps://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra

## Data
Expected local files:
- train.parquet
- test.parquet

Do not commit competition data to Git.

## Split / leakage control
For an internal benchmark, split by molecule identity, not spectrum.
- no spectrum from a held-out molecule may appear in the retrieval library;
- duplicate structures across source libraries remain in the training pool only for the training side;
- report molecule count and spectrum count;
- optionally run a stricter source-library holdout.

The public test set is not a valid local score target because the hidden competition labels are withheld.

## Pipeline
1. Load spectra.
2. Standardize peak arrays.
3. Apply conservative peak filtering.
4. Compute sparse spectral similarity between query and reference spectra.
5. Aggregate evidence across all query spectra belonging to one molecule.
6. Aggregate reference evidence by candidate molecule / InChIKey14.
7. Produce ranked top-25 normalized SMILES.
8. Calculate MRR@25 against the held-out labels.
9. Save metrics, parameters, seed, environment, and failure counts.

## Required controls
- random candidate baseline;
- retrieval-only baseline;
- candidate-cap recall@25;
- molecule-level split;
- leakage audit;
- ablation of preprocessing;
- negative-control query/reference mismatch test.

## Primary metric
MRR@25:
- rank 1 = 1.0
- rank 2 = 0.5
- rank 25 = 0.04
- no correct candidate in top 25 = 0.

## Acceptance
E001 is complete only when:
- the run is reproducible;
- leakage audit passes;
- result JSON/CSV is saved;
- exact configuration is recorded;
- failure cases are preserved for E002+ analysis.

A score is never reported until real CASMI-format data have actually been run.

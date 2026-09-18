# CASMI-E001 — Retrieval Baseline Protocol

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Measure the direct spectral-library retrieval ceiling before adding formula, fingerprint, graph, or generative reasoning.

CASMI evaluates up to 25 ranked SMILES per molecule using MRR@25. Matching uses RDKit tautomer canonicalization and InChIKey14. urlOfficial CASMI 2026 pagehttps://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra

## Two distinct regimes
### A. Known-molecule retrieval
Split spectra **within each molecule**. Reference spectra of the same molecule are allowed, but the queried spectrum itself is excluded. This measures the retrieval ceiling relevant to CASMI novelty class 1.

### B. Novel-molecule holdout
Split by molecule identity. Direct retrieval cannot recover a molecule absent from the reference library; this is a control demonstrating where retrieval ends and E002+ begins.

## Pipeline
1. Load train.parquet and validate test schema.
2. Standardize peak arrays.
3. Apply conservative peak filtering.
4. Compute matched-peak spectral similarity.
5. Aggregate evidence from multiple query spectra.
6. Aggregate reference evidence by InChIKey14.
7. Produce top-25 candidates.
8. Calculate MRR@25.
9. Save metrics, parameters, seed, and failure cases.

## Required controls
- random baseline;
- spectrum-within-molecule retrieval;
- molecule-level novel holdout;
- spectrum-ID leakage audit;
- preprocessing ablation;
- negative-control query/reference mismatch;
- candidate-cap recall@25.

## Acceptance
E001 is complete only after a real-data run is reproducible, leakage-free, and its result artifacts are saved.

A score is never presented as a competition result until real CASMI data have actually been executed.

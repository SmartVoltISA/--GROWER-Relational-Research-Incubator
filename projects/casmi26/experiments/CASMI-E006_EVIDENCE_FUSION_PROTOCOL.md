# CASMI-E006 — Independent Evidence Fusion

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Combine independent evidence channels only after their standalone behavior is measured.

Channels:
1. spectral similarity (E001)
2. precursor/adduct mass constraint (E002)
3. spectrum-derived structural proxy (E003b)
4. graph/fragment relation evidence (E004b)
5. multi-spectrum aggregation (E005)

## Rule
No hand-tuned fixed weights.

Use a held-out calibration set to learn ranking calibration, then freeze it before final evaluation.

## Required controls
- each channel alone;
- every pair;
- full fusion;
- shuffled channel;
- missing-channel robustness;
- calibration-set leakage audit.

## Metrics
MRR@25, Recall@1/5/10/25, candidate recall, calibration error, failure-mode overlap, incremental recall.

## Promotion
A channel is useful only if it contributes reproducible incremental information on held-out molecules.

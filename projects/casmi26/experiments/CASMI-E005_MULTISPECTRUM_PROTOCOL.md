# CASMI-E005 — Multi-Spectrum Evidence Aggregation

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Exploit the fact that CASMI predictions are per molecule while each molecule may have 1–16 spectra at different collision energies/adducts.

## Hypothesis
Aggregating independent spectra for the same molecule improves candidate ranking over any single-spectrum decision.

## Pre-registered aggregation variants
A. maximum evidence
B. mean evidence
C. weighted mean by spectral quality
D. collision-energy-aware aggregation
E. adduct-aware aggregation

## Controls
- best-single-spectrum
- random spectrum
- mean without quality
- shuffled molecule grouping

## Metrics
MRR@25, Recall@1/5/10/25, candidate recall, variance across spectra, gain vs best single spectrum.

## Important
Do not merge spectra blindly. Different adducts and collision energies provide complementary information and may also introduce incompatible evidence.

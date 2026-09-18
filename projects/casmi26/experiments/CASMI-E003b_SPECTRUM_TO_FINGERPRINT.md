# CASMI-E003b — Spectrum → Fingerprint

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Test whether a spectrum can be converted into a structural fingerprint representation that retrieves chemically related reference structures.

## Null hypothesis
A spectrum-derived structural representation adds no incremental information beyond precursor/adduct and direct spectral similarity.

## Representation
Input:
- m/z peaks
- normalized intensities
- precursor m/z
- adduct / ionization mode

Output:
- fixed-length structural fingerprint embedding.

Initial deterministic control:
- hashed peak-pair / neutral-loss features.
- This is not claimed to be a molecular fingerprint; it is a spectrum-derived structural proxy.

## Evaluation
Use molecule-level held-out queries.
For every query:
1. generate spectrum proxy fingerprint;
2. compare against reference molecular fingerprints;
3. rank top-25 candidates;
4. compare with E001/E002;
5. measure incremental candidate recall.

## Required negative controls
- shuffled intensities;
- shuffled m/z;
- spectrum from molecule A paired with metadata from molecule B;
- random candidate ranking.

## Promotion
Only promote to E004 if the representation demonstrates reproducible incremental information under held-out evaluation.

No leaderboard tuning.
No hidden-test inference.

# CASMI-E002 — Precursor / Adduct / Formula Constraints

## Status
REGISTERED / READY FOR REAL DATA

## Hypothesis
Adding precursor-mass and adduct-derived neutral-mass constraints will improve candidate precision and/or top-25 recall over pure spectral retrieval, without reducing valid candidate recall.

## Inputs
Training columns:
- precursor_mz
- adduct
- ionization_mode
- molecular_formula
- precursor_error_ppm
- normalized_smiles
- inchikey14

Test provides precursor_mz, adduct, ionization_mode, but no formula.

## Method
1. Normalize adduct labels.
2. Convert measured precursor m/z + adduct into an estimated neutral monoisotopic mass.
3. For reference structures, calculate neutral monoisotopic mass from molecular formula/SMILES.
4. Compute absolute mass error and ppm error.
5. Use the mass constraint as:
   A. hard candidate filter at predefined ppm thresholds;
   B. soft ranking feature;
   C. retrieval-only control.
6. Compare E002 against E001 on identical molecule/spectrum splits.
7. Run an ablation without adduct.
8. Run a negative control with shuffled adduct labels.

## Important limitation
Formula is known for training/reference structures but not for the hidden test. Therefore E002 must not assume the unknown formula. Formula generation is a later branch.

## Metrics
- MRR@25
- Recall@1, @5, @10, @25
- candidate pool size
- fraction of true structures eliminated by mass filter
- runtime
- failure count

## Acceptance
Promote E002 only if it improves a pre-registered metric without unacceptable loss of candidate recall.

Current competition data facts: test contains seven standardized adducts, and precursor mass/adduct are explicit test columns. urlOfficial CASMI data pagehttps://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra

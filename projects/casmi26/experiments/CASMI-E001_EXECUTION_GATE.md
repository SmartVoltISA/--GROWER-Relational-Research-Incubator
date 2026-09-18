# CASMI-E001/E002 — Current Execution Gate

## Current external state
Checked 18 Sep 2026.

The official Kaggle data page currently reports:
- train.parquet: ~2.5M spectra / ~275k structures;
- test.parquet: ~1,500 spectra / ~400 molecules;
- test is a placeholder drawn from training data and will be replaced by the hidden test on rerun;
- the training data was recently updated; Kaggle staff recommends re-downloading it;
- public data access requires accepting the competition rules;
- dataset license is CC BY-NC 4.0.

Therefore we must not use the visible placeholder test as evidence of hidden-test performance.

## New discovery that changes our validation design
A current public Kaggle discussion reports byte-for-byte overlap between the visible test examples and training data. This is community-reported, not an official competition guarantee, so it is treated as a validation warning rather than a fact about the final hidden test.

Consequence:
- E001 internal validation remains mandatory.
- Public-LB score is not treated as a scientific estimate of generalization.
- Known-molecule retrieval and novel-molecule prediction remain separate regimes.

## Immediate gate
Before E002:
1. obtain the current train.parquet after accepting rules;
2. verify file checksum/version;
3. run E001 known-molecule retrieval;
4. run E001 novel-molecule holdout;
5. run leakage audit;
6. preserve raw metrics and failure cases;
7. only then promote E002 formula/precursor constraints.

## Data policy
Competition data are never committed to Git.
Only scripts, protocols, checksums, metrics, derived non-sensitive summaries, and reproducible experiment metadata are committed.

## Do not infer
No leaderboard score, prize probability, or hidden-test performance is inferred from the placeholder test.

## Next experiment
CASMI-E002:
precursor m/z + adduct + ionization mode + molecular-formula constraints, followed by retrieval/ranking.

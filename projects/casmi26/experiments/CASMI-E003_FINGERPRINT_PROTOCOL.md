# CASMI-E003 — Fingerprint Retrieval / Spectrum-to-Structure Bridge

## Status
REGISTERED / READY FOR REAL DATA

## Goal
Test whether a structure-level fingerprint channel adds information beyond spectral retrieval and precursor/adduct constraints.

## Hypothesis
A spectrum-derived structural fingerprint, combined with a reference molecular fingerprint, can recover chemically similar candidates when exact spectral retrieval fails, especially in novelty Class 2. It must be measured separately from direct retrieval.

## Controls
1. E001 retrieval-only.
2. E002 precursor/adduct filtering.
3. E003 fingerprint-only.
4. E003 retrieval + fingerprint.
5. shuffled-fingerprint negative control.
6. molecule-level split for generalization.
7. exact-structure leakage audit.

## Candidate representation
Reference side:
- RDKit Morgan/ECFP-style fingerprint;
- optionally multiple radii/bit sizes as pre-registered variants.

Query side:
- spectrum → learned or deterministic fingerprint representation.
- No hidden-test labels.
- If a pretrained public model is used, record exact model/version/license.

## Metrics
- MRR@25
- Recall@1/5/10/25
- candidate recall before ranking
- overlap between E001 and E003 candidate sets
- incremental recall: candidates found by E003 but absent from E001
- runtime and memory
- performance by novelty proxy / library source where labels permit

## Promotion rule
Do not hand-tune weights against leaderboard feedback.
A fingerprint channel is promoted only if it produces reproducible incremental information on a held-out molecule-level benchmark.

## External reference
A current public CASMI baseline reports MRR@25 0.339, while another analog-propagation baseline reports 0.335. These are public benchmark observations, not our results. urlPublic cosine baselinehttps://www.kaggle.com/code/haideptry/enveda-casmi-2026-fast-spectral-cosine-baseline urlPublic analog baselinehttps://www.kaggle.com/code/prvsiyan/analog-propagation-casmi-2026-baseline

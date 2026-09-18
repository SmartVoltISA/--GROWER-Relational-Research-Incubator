# CASMI26 — Molecular Structure Research Program

Status: CANDIDATE / TESTING
Incubator: Ω-GROWER
Competition: Enveda CASMI 2026 — Molecule ID From Mass Spectra

## Purpose

Use CASMI 2026 as an external, measurable research environment for the SPACE/GROWER architecture.

The immediate task is MS/MS spectrum → ranked candidate molecular structures (SMILES). The broader incubator program extends this into:

1. spectrum representation;
2. molecular graph reconstruction;
3. candidate generation and ranking;
4. chemical validation;
5. molecular property prediction;
6. controlled molecular generation;
7. comparison of predicted structures with physical/chemical properties.

The broader property/generation program is research beyond the Kaggle scoring task. It must not be confused with the competition target.

## Governing loop

INTENT → RELATIONS → HYPOTHESES → EXPERIMENT → OBSERVATION → FALSIFICATION → CORRECTION → RE-TEST → EVIDENCE → PROMOTION / ARCHIVE

## Architectural path

Opportunity Engine
→ GROWER Incubator
→ STAND / LAB
→ SPACE research components
→ verification
→ Resource Engine
→ result / reusable resource

## Hard boundaries

- No write-back into protected SPACE Core.
- No autonomous external submission.
- No paid service is required for the research core.
- Competition score, prize pool, or leaderboard position is not treated as received resource.
- Every result has provenance, protocol, dataset version and status.
- Failed and negative branches are preserved.

## Competition facts

- Evaluation: MRR@25.
- Up to 25 SMILES candidates per molecule.
- Matching is by RDKit tautomer canonicalization followed by InChIKey14.
- Train: about 2.5M MS/MS spectra and about 275k unique structures.
- Hidden test: about 1,500 spectra and about 400 molecules.
- Novelty classes include library-known, known-without-public-spectra, and novel structures.
- Public data currently totals about 3.04 GB.

Source: Kaggle competition/data pages, checked 2026-09-18.

# CASMI26 Experiment Registry

This is the canonical experiment ledger for the incubator project.

| ID | Hypothesis | Test | Status |
|---|---|---|---|
| CASMI-E000 | Data/metric pipeline can be reproduced locally | Validate schema, aggregation, canonicalization and MRR@25 on a known split | CANDIDATE |
| CASMI-E001 | Spectral-library retrieval establishes the minimum useful baseline | Nearest-spectrum retrieval with molecule-level aggregation | CANDIDATE |
| CASMI-E002 | Formula/precursor constraints reduce candidate space | Add formula/mass/adduct constraints to retrieval | CANDIDATE |
| CASMI-E003 | Fingerprint prediction adds information beyond retrieval | Spectrum → fingerprint → candidate ranking | CANDIDATE |
| CASMI-E004 | Graph-aware candidate reasoning improves Class 2/3 recovery | Candidate graph reconstruction + chemical constraints | CANDIDATE |
| CASMI-E005 | Multi-spectrum aggregation improves molecule-level ranking | Aggregate all spectra belonging to one molecule | CANDIDATE |
| CASMI-E006 | Independent evidence channels improve ranking | Retrieval + fingerprint + graph + formula evidence | CANDIDATE |
| CASMI-E007 | Noise/adduct/collision-energy normalization changes generalization | Controlled ablation | CANDIDATE |
| CASMI-E008 | De-novo generation can recover structures outside reference libraries | Hidden-structure reconstruction/generation | CANDIDATE |
| CASMI-E009 | Property constraints can reject chemically inconsistent candidates | Property/descriptor consistency checks | CANDIDATE |
| CASMI-E010 | Generated molecular families can be grown under declared physical/chemical constraints | Incubator generation experiment | CANDIDATE |

## Required controls

- random baseline;
- retrieval-only baseline;
- candidate-cap recall;
- duplicate/leakage control;
- molecule-level split;
- library/source holdout;
- negative control;
- ablation of every added evidence channel.

## Result rule

No result is promoted from CANDIDATE until the experiment has an executable protocol and an observed result.


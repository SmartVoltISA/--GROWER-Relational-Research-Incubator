# CASMI26 Architecture

## 1. External opportunity

Opportunity Engine records the competition as an economic/research opportunity, but does not convert advertised prize money into a resource.

## 2. GROWER

GROWER generates competing solution structures:

- retrieval;
- spectral similarity;
- formula/constraint reasoning;
- molecular fingerprints;
- graph reconstruction;
- learned spectrum embeddings;
- candidate propagation;
- de-novo generation.

No single model is considered authoritative.

## 3. LAB / STAND

All computational experiments run in an isolated research contour.

Required experiment record:

- experiment_id
- hypothesis_id
- dataset_version
- code_version / commit
- model_version
- parameters
- random seed
- split definition
- negative control
- metric
- result
- uncertainty / limitations
- decision
- artifact/provenance

## 4. FALSIFIER

For every proposed improvement:

BASELINE
→ proposed mechanism
→ counter-test
→ leakage test
→ ablation
→ independent split
→ result

A higher leaderboard score without a valid causal explanation is not sufficient evidence of architectural improvement.

## 5. Candidate graph

The core representation should preserve:

spectrum → peaks → mass differences / neutral losses → constraints → molecular graph → canonical structure

SMILES is the output serialization, not the internal ontology.

## 6. Property branch

After structure reconstruction:

molecular graph
→ descriptors
→ predicted properties
→ uncertainty
→ experimental/property database comparison

The property branch is a separate research objective from CASMI scoring.

## 7. Molecular growth branch

Candidate graph
→ admissible transformations
→ generated structures
→ validity filters
→ property prediction
→ constraint checks
→ evidence ledger

The incubator must never treat a generated molecule as experimentally confirmed.

## 8. Promotion

CANDIDATE
→ TESTING
→ SUPPORTED
→ PARTIAL / NOT_PROVEN / FAIL / INVALID
→ ARCHIVED or PROMOTED

Promotion requires reproducible evidence and preserves the rejected branches.

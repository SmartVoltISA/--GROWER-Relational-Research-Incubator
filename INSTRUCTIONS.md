# Ω-GROWER — INSTRUCTION MANUAL

## 0. Purpose

This document is the operating instruction for the Incubator.

The Incubator is not a chat folder and not a collection of ideas. It is a controlled research system for turning an intention into reproducible evidence and, only after verification, into a reusable component or resource.

The canonical loop is:

INTENT → RELATIONS → CANDIDATE → HYPOTHESIS → EXPERIMENT → OBSERVATION → FALSIFICATION → CORRECTION → RE-TEST → EVIDENCE → PROMOTION / ARCHIVE

Never skip a stage silently.

---

## 1. First rule: do not start by building

Before writing code or training a model:

1. define the question;
2. define what would count as a positive result;
3. define the null / baseline;
4. define the data and version;
5. define the metric;
6. define the allowed resources;
7. define the boundary and safety constraints;
8. define the stop / rejection criteria;
9. create an experiment ID;
10. only then implement.

Existing repositories and contracts are read first. New mechanisms must reconcile with existing Foundation / SPACE contracts before implementation.

---

## 2. Status vocabulary

Use only these status values unless a project declares a stricter controlled vocabulary:

- CANDIDATE — proposed, not yet tested.
- TESTING — executable experiment is running or being analysed.
- SUPPORTED — evidence supports the stated claim within the declared domain.
- PARTIAL — only part of the claim is supported.
- NOT_PROVEN — test completed without sufficient evidence.
- FAIL — declared success criterion was not met.
- INVALID — protocol, data, implementation, or boundary was invalid.
- ARCHIVED — preserved for history and not currently active.

SUPPORTED never means universal truth.

---

## 3. Experiment record

Every experiment gets a unique immutable ID.

Minimum record:

- experiment_id
- date
- intent
- hypothesis
- null / baseline
- dataset and exact version
- data split
- code commit
- model version
- parameters
- random seed
- metric
- acceptance criterion
- negative control
- execution result
- uncertainty / limitations
- falsification attempt
- decision
- artifacts
- next experiment

An experiment cannot be marked EXECUTED when it has only been proposed.

---

## 4. Baseline before complexity

For every new task:

BASELINE → MEASURE → ADD ONE MECHANISM → MEASURE → COMPARE → REPEAT

At minimum keep:

1. naive/random baseline where meaningful;
2. simplest useful domain baseline;
3. current best internal baseline.

Never compare a complex model only against a straw-man.

---

## 5. Leakage control

Before trusting a result:

- identify duplicates;
- identify shared entities across train/validation;
- split at the correct semantic unit;
- check source/library overlap;
- check temporal or experimental leakage where applicable;
- run a deliberately harder holdout;
- record all exclusions.

If a split can leak information from the answer into the candidate generator, the result is not promotion-grade.

---

## 6. Falsifier

For every positive result, ask:

What else could have produced this improvement?

Then test it.

Required where applicable:

- ablation;
- negative control;
- alternative split;
- shuffled/control labels;
- retrieval-only comparison;
- source/library holdout;
- seed sensitivity;
- parameter sensitivity;
- independent reproduction.

The Falsifier has priority over confirmation.

---

## 7. Memory

Never overwrite an experiment.

Store:

FACT → OBSERVATION → RESULT → DECISION

Keep failed branches.

A negative result is an anchor because it tells the next cycle what not to repeat.

---

## 8. Promotion gate

A candidate can move forward only when:

1. protocol is reproducible;
2. result is observed;
3. baseline comparison exists;
4. failure modes are documented;
5. provenance is complete;
6. declared acceptance criteria are met;
7. the result survives the required falsification checks.

Promotion levels:

CANDIDATE → TESTING → SUPPORTED → REUSABLE → PROJECT-INDEPENDENT → FOUNDATIONAL

Promotion never deletes the original branch.

---

# CASMI26 OPERATING PROCEDURE

## 9. Competition target

CASMI26 asks for up to 25 ranked SMILES candidates per molecule from MS/MS evidence. Evaluation uses MRR@25 after RDKit tautomer canonicalization and comparison of the first InChIKey block. Evidence from multiple spectra belonging to one molecule must be aggregated.

Source: official Kaggle competition/data pages, checked 2026-09-18.

Therefore the internal representation must not be SMILES-first.

Use:

SPECTRA → FEATURES / RELATIONS → MOLECULAR GRAPH → CANDIDATES → RANKING → SMILES SERIALIZATION

SMILES is the exchange format, not the internal ontology.

---

## 10. CASMI experiment sequence

### CASMI-E000
Verify the evaluator mechanics on synthetic examples.

### CASMI-E001
Build retrieval-only baseline.

Protocol:

1. load a controlled subset of train;
2. canonicalize labels;
3. build spectrum representation;
4. retrieve nearest reference spectra;
5. aggregate evidence per molecule;
6. produce up to 25 candidates;
7. calculate MRR@25;
8. record runtime and memory.

### CASMI-E002
Add precursor/formula/adduct constraints.

### CASMI-E003
Add spectrum → fingerprint evidence.

### CASMI-E004
Add graph-aware candidate reasoning.

### CASMI-E005
Test multi-spectrum aggregation.

### CASMI-E006
Fuse independent evidence channels.

### CASMI-E007
Test preprocessing choices and collision-energy handling.

### CASMI-E008
Test de-novo recovery on held-out structures.

### CASMI-E009
Add property-consistency filters.

### CASMI-E010
Begin controlled molecular-space growth.

One experiment changes one primary mechanism unless the experiment is explicitly declared factorial.

---

# 11. Molecular / periodic-system incubator

The phrase “grow the periodic table” is treated as an architectural research direction, not as a claim that the model can recreate the physical periodic table.

Separate the problem into levels:

### Level 1 — Elements

Reference facts:

atomic number, isotope information, electron configuration, oxidation states, radii, electronegativity and other declared properties.

### Level 2 — Atoms

Element + charge + isotope + local environment.

### Level 3 — Bonds

Bond type, order, geometry and allowed valence constraints.

### Level 4 — Molecular graphs

Atoms + bonds + connectivity + charge + stereochemical information where relevant.

### Level 5 — Molecular properties

Compute or predict declared properties with:

- units;
- model version;
- training domain;
- uncertainty;
- applicability domain.

### Level 6 — Physical evidence

Compare predictions against independent measured data.

### Level 7 — Controlled growth

Generate new candidate structures only inside a declared feasible set.

### Level 8 — Falsification

Try to break each candidate using independent constraints and measurements.

---

## 12. Physical-property rule

Never write:

PREDICTED PROPERTY = PHYSICAL FACT

Use:

PREDICTED PROPERTY
→ uncertainty
→ independent reference
→ comparison
→ supported / not proven

For a generated molecule:

GENERATED ≠ CHEMICALLY CONFIRMED ≠ PHYSICALLY MEASURED

Only an independent physical/chemical experiment can establish a measured property.

---

## 13. Growth engine

The growth engine works by relations and constraints, not arbitrary random molecule generation.

Basic cycle:

SEED
→ TRANSFORMATION
→ CANDIDATE
→ VALIDITY CHECK
→ PROPERTY PREDICTION
→ CONSTRAINT CHECK
→ FALSIFIER
→ SURVIVOR SET
→ NEXT GENERATION

Every generation records:

- parent;
- transformation;
- reason for transformation;
- constraints;
- predicted properties;
- uncertainty;
- rejection reason;
- surviving candidate ID.

This makes the chemical search space traceable.

---

## 14. Evidence levels

For every molecular candidate maintain separate evidence channels:

E1 — structural validity
E2 — spectral consistency
E3 — database/reference consistency
E4 — predicted-property consistency
E5 — independent measured-property agreement
E6 — independent experimental confirmation

Do not collapse these into one opaque score.

A candidate may be strong on E2 and weak on E5. That distinction must remain visible.

---

## 15. Resource conversion

The Incubator does not declare money.

The economic chain is:

OPPORTUNITY
→ ELIGIBILITY
→ EXPERIMENT
→ VERIFIED RESULT
→ EXTERNAL OUTCOME
→ REALIZED RESOURCE

Advertised prize ≠ expected value ≠ received money.

For CASMI26, licensing is part of the resource gate. The official competition page states requirements for publicly available external data/models and submission conditions; the organizer also warns that a winning solution must be compatible with commercial licensing and redistribution requirements.

Therefore every external dataset, model and tool gets a LICENSE CHECK before inclusion in a competition-grade branch.

---

## 16. STAND boundary

All destructive, expensive, uncertain or experimental work belongs in STAND/LAB.

Never write experimental state directly into protected SPACE Core.

Required path:

GROWER
→ STAND
→ LAB
→ RESULT
→ REVIEW
→ PROMOTION

External submissions, spending, transfers and acceptance of external terms require explicit authorization.

---

## 17. Definition of done

A research branch is complete only when:

- the question is answered or explicitly unresolved;
- the experiment is reproducible;
- the data version is recorded;
- the code commit is recorded;
- controls are recorded;
- failures are recorded;
- evidence is preserved;
- the next decision is explicit.

The final state must be one of:

SUPPORTED / PARTIAL / NOT_PROVEN / FAIL / INVALID / ARCHIVED

Never use “works” as a scientific status.

---

## 18. Core principle

The Incubator grows knowledge, not stories.

FACT → CHECK → RESULT → DECISION → FIXATION

Then:

FIXATION → NEW QUESTION → NEW EXPERIMENT

No circular wandering. No silent assumptions. No erased failures.

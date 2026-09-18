# CASMI-E009 — Property Consistency

## Status
REGISTERED / DESIGN PHASE

## Goal
Use predicted physical/chemical properties as consistency constraints, never as fabricated measurements.

## Chain
structure → descriptors → property model → external/reference evidence → consistency check.

## Rule
Predicted ≠ measured.
Every property gets provenance and uncertainty.

## Candidate uses
- reject chemically implausible candidates;
- rank candidates when evidence is otherwise tied;
- identify regions of chemical space requiring external measurement.

## Metrics
constraint precision, false rejection rate, candidate recall, calibration error.

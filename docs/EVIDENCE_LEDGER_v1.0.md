# Ω-GROWER Evidence Ledger v1.0

Every growth cycle produces an append-only logical record with:

- cycle ID and parent branch
- intent and success criteria
- relation seed and provenance
- hypothesis IDs and null hypotheses
- preregistration/version
- experiment/protocol IDs
- raw observation references
- environmental and calibration state when applicable
- uncertainty budget
- controls and counterexamples
- result and status
- exact promotion decision
- reason for archive/rejection when applicable

## Evidence rule
A claim is promoted only with a traceable chain:
`claim → prediction → protocol → observation → analysis → control → decision`.

A model-generated explanation is not evidence by itself.

## Branch rule
Every correction creates a new branch/version. Previous branches remain addressable. This prevents the agent from rewriting history to make a result look successful.

## Reuse rule
Independent reuse must reference the original evidence but execute its own test. Reuse is evidence of robustness, not permission to skip testing.

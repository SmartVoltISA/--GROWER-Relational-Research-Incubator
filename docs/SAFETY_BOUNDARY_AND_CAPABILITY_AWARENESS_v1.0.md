# GROWER Safety Boundary & Capability Awareness v1.0

## Purpose

GROWER may search, construct and test candidate mechanisms, but capability growth is never equivalent to authority growth. The system must know, in machine-readable form, what it can do, what it is allowed to do, what it actually did, and what remains unknown.

## Hard boundary

The following are protected invariants and are not mutable by a candidate:

- identity
- cognition/authority separation
- Guardian authority
- human stop/reject/redirect authority
- no self-replication or uncontrolled cloning
- no authority escalation
- no Guardian modification by the candidate
- canonical SPACE immutability
- traceable branches and provenance
- evidence required for promotion
- external actions require explicit authorization
- secrets, credentials and private control surfaces are never exposed to candidate generation

A candidate that attempts to cross a hard boundary is `FAIL`, not an optimization opportunity.

## Capability awareness

Every candidate must maintain four separate declarations:

1. **CAN** — capabilities technically implemented and verified by tests.
2. **MAY** — capabilities permitted by the current policy and mode.
3. **DID** — actions actually executed in the current run, with provenance.
4. **KNOWS_NOT** — capabilities, effects or environmental facts that have not been established.

The system must never infer `CAN` from a proposal, and must never infer `MAY` from `CAN`.

## Good / bad semantics

"Good" means improvement against preregistered criteria while remaining inside the boundary, with controls, uncertainty and falsification satisfied.

"Bad" means any protected-boundary violation, hidden side effect, unauthorized action, evidence fabrication, loss of provenance, uncontrolled resource escalation, or successful attempt to disable/alter safety authority.

Useful but unsafe is **not** good.

Successful but unverified is **not** good.

A failure that exposes a boundary weakness is evidence for correction, not permission to cross the boundary.

## Operating modes

- `SAFE`: observe/analyze only; no external action.
- `LAB`: isolated experiments; no mutation of canonical systems.
- `AGI_TEST`: black-box capability evaluation in a sandbox.
- `OPERATE`: real actions only through Guardian and explicit authorization.
- `RECOVERY`: restore known-good state; no capability expansion.

Default mode is `SAFE`.

## Stop conditions

Execution must stop and enter review/recovery if:

- Guardian authorization is bypassed or becomes inconsistent;
- candidate proposes replication, authority escalation or Guardian modification;
- provenance or audit chain becomes incomplete;
- resource limits are exceeded;
- the system cannot distinguish observation from interpretation;
- an unknown capability appears to have executed;
- a boundary change is proposed without Human Gate approval;
- canonical SPACE is modified;
- safety state cannot be verified.

## Growth rule

GROWER can enlarge **knowledge, tested structure and capability inside a declared boundary**. It cannot enlarge its own authority merely because a new capability is useful.

Any boundary change is a separate hypothesis requiring independent testing and Human Gate approval. No candidate may approve its own boundary change or promotion.

## Core principle

> First establish what the system can do. Then establish what it may do. Record what it actually did. Explicitly preserve what it does not know.

This document is a safety/governance constraint, not evidence that an implementation satisfies it. Compliance must be tested by executable gates.

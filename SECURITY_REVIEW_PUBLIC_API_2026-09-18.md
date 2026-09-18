# Ω-GROWER Public API Security Review — 2026-09-18

## Scope
Static adversarial review of all public functions/methods currently exposed by src/.

## Authority matrix

| API | State mutation | Promotion authority | Gate |
|---|---:|---:|---|
| GrowthCycle.add_hypothesis | Yes, before lock | No | duplicate-ID check |
| GrowthCycle.lock_for_testing | State transition | No | input validation + fingerprint |
| GrowthCycle.record_evidence | Yes | No | state/type check |
| GrowthCycle.record_test_result | Yes | No | BoundaryDecision issuer + evidence gate + cycle binding |
| GrowthCycle.decide | Yes | SUPPORTED only with gated evidence | locked-input + evidence integrity |
| seed_cycle | Creates cycle | No | delegates to GrowthCycle |
| propose_test_plan | No | No | TESTING only |
| attach_observation | Adds evidence | No | schema + GrowthCycle gate |
| grow | No | No | actions only |
| priority/select_next/should_stop | No | No | advisory only |
| issue_certificate | No | Attestation only | supported gated evidence + fingerprint |
| assemble | No | No automatic promotion | certificate + cycle/evidence binding |
| BoundaryGate.evaluate | No | No | protected invariants + OperatorAuthority |
| OperatorAuthority.authorize | No research mutation | Issues surgery token | proof + confirmation + bindings |
| OperatorAuthority.consume | Consumes token | No | issuer + one-shot + bindings |
| evidence_gate.evaluate | No | No | schema/metrics |
| archive_branch | Writes supplied archive | No | terminal status + duplicate ID |
| CapabilityState.record | Descriptive history | No | CAN + MAY |
| grow_hypotheses | Returns candidates | No | never evidence |
| grow_space | Returns candidate | No | boundary evaluation; NOT_PROVEN default |

## Findings

**FACT-001 — No alternate promotion API found.** Promotion to SUPPORTED is centralized in GrowthCycle.decide and requires a genuine cycle-bound test result with ADMISSIBLE boundary and valid fingerprint.

**FACT-002 — Certificate assembly is attestation-bound.** Certificates carry cycle ID, evidence ID and evidence fingerprint; assembly requires matching cycle and evidence IDs.

**FACT-003 — Operator surgery is external and one-shot.** Protected growth-boundary changes require explicit confirmation, external proof, target binding and one-shot consumption.

**FACT-004 — Advisory APIs are not authority.** growth_engine, hypothesis_grower, grow and CapabilityState do not directly grant promotion authority.

**FACT-005 — Same-process trust limitation remains.** Python private fields and module-level issuer objects are not a process-isolation boundary. Fully privileged code in the same interpreter can introspect or mutate private state. This is a containment limitation, not evidence of an external exploit in the reviewed API.

**REVIEW-001 — archive_branch receives a mutable external archive.** It appends a detached record, but the caller owns the container. Tamper-evident canonical history needs a dedicated append-only storage boundary and integrity metadata.

**REVIEW-002 — CapabilityState is descriptive.** Its mutable CAN/MAY sets are not themselves an execution authorization boundary.

**REVIEW-003 — SpaceCandidate ID derivation.** Current ID uses parent + relations. Because the generator does not currently accept goal/organs/invariants as independent inputs, this is not presently an alternate path; if those become configurable, include the full canonical manifest in the ID.

## Verification status
This review is source-level/static. It records architecture facts and regression tests added to the repository. It does not claim GitHub Actions or external runtime execution of all tests on 2026-09-18.

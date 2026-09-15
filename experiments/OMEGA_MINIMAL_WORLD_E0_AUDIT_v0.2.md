# Ω Minimal World E0 — Static Protocol Audit v0.2

**Status:** READY FOR EXECUTION — static audit complete; empirical run not yet interpreted.

## Scope

Audit the v0.2 preregistration against `OMEGA_MINIMAL_WORLD_E0_v0.2.py` before any decisive batch result is inspected.

## Checks

- [x] N=100 and 5000 normal timesteps are fixed.
- [x] Seeds 1001–1020 are fixed.
- [x] Movement opportunity is shared across conditions.
- [x] Interaction radius is shared across conditions.
- [x] Relations are created only by actual local encounters.
- [x] No condition injects a target number of edges per timestep.
- [x] C0 disables memory and feedback-mediated state/relation adaptation.
- [x] C1 removes memory while retaining feedback.
- [x] C2 removes feedback while retaining memory.
- [x] C3 changes only the resource replenishment regime.
- [x] FULL enables memory, feedback, and adaptive relation reinforcement.
- [x] Scarce replenishment (0.025 mean/agent/step) is below baseline consumption (0.035 plus impulse cost).
- [x] Abundant replenishment (0.25 mean/agent/step) is materially above baseline consumption.
- [x] Resource availability is spatially heterogeneous through a fixed 10×10 field.
- [x] Relation persistence uses the preregistered t=999 checkpoint cohort.
- [x] Empty checkpoint cohorts are recorded as undefined rather than silently converted to zero.
- [x] Primary metrics are emitted by the implementation.
- [x] Actual resource-transfer amounts are recorded per relation for flow concentration.
- [x] Ten-percent deletion is deterministic from the run seed.
- [x] Deleted nodes and their relations are removed before recovery.
- [x] A fixed 100-step recovery window is applied identically across conditions.
- [x] Main-run state is copied before robustness testing, so robustness cannot alter primary metrics.
- [x] Implementation records condition and seed with every output row.

## Important interpretation boundary

This audit is a **static protocol/code consistency check**. It does not establish that the implementation is bug-free at runtime and does not constitute experimental evidence.

The next gate is an executable smoke test on at least one seed per condition, followed by a deterministic batch run. If the smoke test exposes a mismatch, the experiment remains unpromoted and the implementation is corrected before decisive results are inspected.

## Evidence rule

No output from v0.2 may be called evidence for H1 until:

`static audit → smoke test → frozen implementation → full batch → independent review → falsification analysis`

## Relation to v0.1

The v0.1 branch remains `INVALID` and is not pooled with v0.2.

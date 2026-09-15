# Ω Minimal World — E0 Audit Result v0.1

## Status
INVALID — protocol/implementation mismatch

## Scope
This audit evaluates `OMEGA_MINIMAL_WORLD_E0.py` against the preregistered protocol `OMEGA_MINIMAL_WORLD_E0_PREREG_v0.1.md`. It does not modify or reinterpret the preregistration.

## Audit finding
The implementation cannot provide a valid test of H1 under the preregistered protocol.

### 1. Resource scarcity is not actually binding
The implementation uses a baseline environmental inflow of `N * 0.08 = 8` resource units per step for 100 agents, while each active agent consumes approximately `0.03–0.05` units per step. With all agents alive, baseline inflow is therefore greater than total consumption. The intended scarcity mechanism is consequently weak or absent over the tested trajectory.

### 2. FULL has an explicit graph-density generator
In every FULL step the implementation adds approximately `len(alive)/10` new relations. This directly forces edge growth independently of whether collective organization has emerged. A rising edge count or connectivity therefore cannot be interpreted as evidence of emergent organization.

### 3. The declared primary metrics are not implemented
The preregistration requires final survival, mean persistence duration, relation persistence, giant-component fraction, state diversity/occupancy, and resource-flow concentration. The executable returns only final survival, mean survival, edge count, and initial-edge persistence. Several preregistered metrics are therefore unavailable.

### 4. C0 is not a matched random baseline for the full question
C0 applies decay to relations but does not reproduce a matched static/random relation process with the same effective interaction opportunity as FULL. The comparison therefore mixes adaptive dynamics with a substantial difference in relation-generation dynamics.

### 5. One observed execution already exposes a trivial regime
For seed 1001, the implementation produced survival = 1.0 for every condition, while the FULL condition reached 4950 edges (the complete undirected graph for N=100). Controls lost all edges. This is a deterministic consequence of the declared update rules, not evidence of collective organization.

## Decision
The E0 result is `INVALID`, not `NOT_PROVEN`.

No support for H1 is claimed. No metric difference from this implementation is promoted to the evidence ledger.

## Required correction before E0 can be rerun
1. Make baseline resource supply genuinely capable of producing scarcity and mortality under declared parameters.
2. Separate relation formation from the measurement of organization; do not inject a fixed number of edges per step solely in FULL.
3. Implement every preregistered primary metric.
4. Match control interaction opportunities and computational budget as closely as possible.
5. Add explicit giant-component, state-occupancy, resource-flow, and deletion-robustness calculations.
6. Freeze the corrected protocol and implementation as a new version before inspecting decisive results.

## Principle
The failed implementation is retained as a useful negative branch. It demonstrates why the Incubator requires protocol-to-code auditing before promotion.

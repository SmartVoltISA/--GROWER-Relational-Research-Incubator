# Ω-GROWER State Machine v1.0

```text
SEED
  ↓
GROW
  ↓
PLAN
  ↓
RUN
  ↓
OBSERVE
  ↓
FALSIFY ──→ FAIL ──→ ARCHIVE
  ↓
CORRECT
  ↓
RETEST ──→ INVALID ──→ ARCHIVE
  ↓
PROMOTE
  ├── PARTIAL
  ├── NOT_PROVEN
  └── SUPPORTED
          ↓
       REUSE
          ↓
    PROJECT_INDEPENDENT
          ↓
      FOUNDATIONAL
          ↓
       ASSEMBLE
          ↓
       NEW SEED
```

### Transition rules
- `SEED → GROW`: sufficient intent and relation provenance exist.
- `GROW → PLAN`: at least one candidate and one competing/null hypothesis exist.
- `PLAN → RUN`: preregistration is locked.
- `RUN → OBSERVE`: raw output is preserved.
- `OBSERVE → FALSIFY`: observations are bound to the exact protocol.
- `FALSIFY → FAIL`: a decisive failure criterion is met.
- `FALSIFY → CORRECT`: evidence exposes a repairable assumption/model defect.
- `FALSIFY → PROMOTE`: only when declared support criteria pass and no decisive contradiction remains.
- Any integrity/provenance violation → `INVALID`.
- Any rejected or superseded branch → `ARCHIVE`, never silent deletion.

The state machine is intentionally conservative: uncertainty is not converted into success.

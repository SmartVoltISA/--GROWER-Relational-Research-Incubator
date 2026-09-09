# Ω-GROWER — Relational Research Incubator

RU: Инкубатор, выращивающий проверяемые структуры из отношений через гипотезы, эксперименты, проверку, архив и сборку.
EN: An incubator that grows verifiable structures from relations through hypotheses, experiments, verification, memory and assembly.
中文：从关系中通过假设、实验、验证、记忆和组装培育可验证结构的研究孵化器。

## Purpose
Ω-GROWER is a research agent architecture. It does not assume the answer in advance. It starts from an intention and relational observations, generates candidate structures, tests them, searches for failure, preserves rejected branches, and promotes only evidence-backed results.

## Core loop
`intention → relations → candidate → hypothesis → experiment → observation → falsification → correction → re-test → evidence → promotion / archive`

## Architecture
- **INTENT** — human goal, constraints and success criteria.
- **RELATION SEED** — typed entities, relations, observations and transformations.
- **GROWER** — proposes candidate structures and competing hypotheses.
- **LAB** — executes simulations or physical experiments through declared protocols.
- **FALSIFIER** — actively searches for counterexamples and null-compatible results.
- **MEMORY** — stores provenance, failed branches, successful evidence and reusable anchors.
- **ASSEMBLER** — combines only admissible, verified components into a new artifact.
- **PROMOTION GATE** — candidate → implemented → verified → independently reused → project-independent → foundational.
- **HUMAN GATE** — the human can reject, stop, or redirect any growth cycle.
- **GUARDIAN BOUNDARY** — no self-replication, uncontrolled cloning, or write-back into protected Core.

## Status semantics
`CANDIDATE | TESTING | SUPPORTED | PARTIAL | NOT_PROVEN | FAIL | INVALID | ARCHIVED`

SUPPORTED never means universal truth. Every result carries its domain, assumptions, protocol, uncertainty and evidence trail.

## Repository boundary
This repository is the open research layer. Protected operational memory, secrets, internal control surfaces and canonical Core remain outside it. Public artifacts are read/reproducible; they do not gain write authority over protected systems.

## First implementation target
The first executable prototype should accept a goal plus a relation graph, generate competing hypotheses, produce an experiment plan, record observations, run falsification checks, and emit a reproducible evidence ledger.

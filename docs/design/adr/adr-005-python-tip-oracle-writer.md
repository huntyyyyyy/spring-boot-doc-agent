---
title: 'ADR-005: Python tip remains coverage.xml and claims writer'
status: Proposed
date: '2026-08-10'
adr: ADR-005
related:
  - docs/design/adr/README.md
  - .cursor/rules/se-quality-constitution.mdc
  - docs/design/e-lie0-requirements-2026-08-10.md
claim_tiers: Confirmed
last_reviewed: '2026-08-10'
---

# ADR-005: Python tip remains oracle writer

## Context

Constitution: one tip writer; fail_under 98.7 on `coverage.xml`; claims
predicates. Polyglot pilots (Go/WASM/bb/Rust) must not create a second merge
SoT. Constraint, not a MoSCoW wish.

## Decision

We will keep **Python** as the sole writer of `coverage.xml` and claims until a
**named cutover Approve** ADR supersedes this one. All other languages are
sidecars/sensors/sandboxes.

## Status

Proposed.

## Consequences

Positive: preserves CI SoR; allows rich pilots.  
Negative: hot paths may need FFI later; cutover is high-ceremony.  
Rejected: Rust/Go tip rewrite in Pilot; dual Cover% under “engine.”

---
title: 'Architecture Decision Record ADR-0008: C4 and Architecture Decision Records before product code'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0008: C4 + Architecture Decision Records before product code

## Context

Code without decisions and containers goes stale. This port is a Spec corpus
until Definition of Ready and no-code-gate pass.

## Decision

No product crates/daemons/extensions until: working-draft requirements form,
six-part Quality Attribute Scenarios for Must non-functionals, C4 Context +
Container (SoT: `docs/c4/`), and Architecture Decision Records for each
container — human Accept where required by the gate.

## Status

Proposed.

## Consequences

Positive: blocks fashion polyglot scaffolds.  
Negative: slower tip dopamine.  
Rejected: “spike folder becomes the tip” without Accept.

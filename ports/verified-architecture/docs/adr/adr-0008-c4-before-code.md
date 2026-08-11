---
title: 'Architecture Decision Record ADR-0008: C4 and Architecture Decision Records before product code'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record ADR-0008: C4 + Architecture Decision Records before product code

## Context

Crates without Accept decisions and Container diagrams go stale under agent
edits. This port stays a Spec corpus until Definition of Ready and the no-code
gate pass.

## Decision

Refuse product crates, daemons, and extensions until all of: working-draft
requirements form, six-part Quality Attribute Scenarios for Must
non-functionals, C4 Context + Container (System of Record: `docs/c4/`), and
Architecture Decision Records for each container — human Accept where the gate
requires it. A “spike folder becomes the tip” without Accept fails this
Architecture Decision Record.

## Status

Proposed.

## Consequences

Positive: fashion polyglot scaffolds cannot land as tip.  
Negative: slower early dopamine; Spikes stay chartered, not productized.  
Rejected: Implement before Definition of Ready PASS; tip from unaccepted spike
folders.

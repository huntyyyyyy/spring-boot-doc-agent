---
title: 'Architecture Decision Record ADR-0003: Packwerk-shaped lock IR with Ruby bounded context'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/03-locks-ruby
---

# Architecture Decision Record ADR-0003: Packwerk-shaped lock IR (Ruby bounded context)

## Context

Package boundary debt needs an executable Intermediate Representation humans and
agents share. Packwerk is the pattern source; evaluation lives in the engine.

## Decision

**Packwerk-shaped lock Intermediate Representation** (JSON schema in ICD).
**Ruby** owns Packwerk-shaped DX / authoring bounded context. **Rust**
`LockCheck` evaluates (Architecture Decision Record ADR-0004 / ADR-0007).

## Status

Proposed.

## Consequences

Positive: gradual enforce modes; shared IR.  
Negative: adapter fidelity matrix required.  
Rejected: prose-only locks; per-language checkers with no shared IR; Python lock
authoring SoT.

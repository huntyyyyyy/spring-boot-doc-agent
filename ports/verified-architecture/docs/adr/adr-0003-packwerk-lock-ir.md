---
title: 'Architecture Decision Record ADR-0003: Packwerk-shaped lock IR with Ruby bounded context'
status: Proposed
date: '2026-08-10'
last_reviewed: '2026-08-11'
nest: nests/03-locks-ruby
---

# Architecture Decision Record ADR-0003: Packwerk-shaped lock IR (Ruby bounded context)

## Context

Package-boundary debt needs an Intermediate Representation humans and agents
share. Packwerk supplies the pattern; evaluation must stay in the engine so
per-language checkers cannot diverge.

## Decision

Lock rules ship as **Packwerk-shaped JSON** under the Interface Control
Document schema. **Ruby** authors Packwerk-shaped manifests (nest
`03-locks-ruby`). **Rust** `LockCheck` evaluates them (Architecture Decision
Record ADR-0004 / ADR-0007). Prose-only locks or a Python authoring System of
Record fail this Architecture Decision Record.

## Status

Proposed.

## Consequences

Positive: gradual enforce modes against one Intermediate Representation.  
Negative: adapter fidelity matrix required per language front-end.  
Rejected: prose-only locks; per-language checkers with no shared Intermediate
Representation; Python lock authoring System of Record.

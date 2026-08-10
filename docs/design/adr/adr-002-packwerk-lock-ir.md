---
title: 'ADR-002: Packwerk-shaped lock IR (pattern, not tip Ruby)'
status: Proposed
date: '2026-08-10'
adr: ADR-002
related:
  - docs/design/adr/README.md
  - docs/research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md
  - docs/research/process/53-e-lie0-pilot-mental-models-polyglot-lanes-2026-08-10.md
claim_tiers: Evidenced
last_reviewed: '2026-08-10'
---

# ADR-002: Packwerk-shaped lock IR

## Context

Architecture locks must be executable, gradual (`todo` bankruptcy), and honest
about static-analysis FN/FP. Shopify Packwerk supplies the mental model
(packages, enforce_dependencies, privacy, package_todo, prefer FN over FP).
Constraint: do not make Ruby a tip kernel.

## Decision

We will **Adopt the Packwerk pattern** as YAML/MDC **lock IR** evaluated by
`LockCheck` in the tip language(s). We will **not** add Packwerk gem as a merge
dependency.

## Status

Proposed.

## Consequences

Positive: known gradual-modularization playbook; maps to controller→repo demos.  
Negative: must reimplement checker; Spring Magic still yields Unknown/FN.  
Rejected: prose-only `.mdc` theater; ArchUnit-as-only-SoT without IR export.

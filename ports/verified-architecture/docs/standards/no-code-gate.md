---
title: No-code gate — Spec → Constraints → Quality Attribute Scenario → C4 → Architecture Decision Record → then code
status: ACTIVE
date: '2026-08-10'
---

# No-code gate

This repository begins as **requirements and constraint engineering** plus
architecture analysis. Product code is refused until the gate checklist in
`CONTRIBUTING.md` is green.

## Why

C4 without decisions goes stale. Latency adjectives without Architecture Tradeoff Analysis Method scenarios are
not non-functional requirements. Polyglot without bounded context ownership is fashion. Formal labels without
artifacts are marketing.

## Allowed before gate

- Requirements, constraints, Quality Attribute Scenario, Requirements Traceability Matrix
- C4 models (Context / Container / Component)
- Architecture Decision Records (Nygard)
- Research memos and Architecture Tradeoff Analysis Method tradeoff tables
- Doc linters / link checkers

## Forbidden before gate

- Engine crates, daemons, gems, JVM services, WebAssembly binaries as product
- “Just a spike folder” that becomes the tip without Architecture Decision Record Accept
- Python-majority scaffolding that re-centers the old product identity

---
title: No-code gate — Spec → Constraints → QAS → C4 → ADR → then code
status: ACTIVE
date: '2026-08-10'
---

# No-code gate

This repository begins as **requirements and constraint engineering** plus
architecture analysis. Product code is refused until the gate checklist in
`CONTRIBUTING.md` is green.

## Why

C4 without decisions goes stale. Latency adjectives without ATAM scenarios are
not NFRs. Polyglot without BC ownership is fashion. Formal labels without
artifacts are marketing.

## Allowed before gate

- Requirements, constraints, QAS, RTM
- C4 models (Context / Container / Component)
- ADRs (Nygard)
- Research memos and ATAM tradeoff tables
- Doc linters / link checkers

## Forbidden before gate

- Engine crates, daemons, gems, JVM services, WASM binaries as product
- “Just a spike folder” that becomes the tip without ADR Accept
- Python-majority scaffolding that re-centers the old doc-engine identity

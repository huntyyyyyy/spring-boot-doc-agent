---
title: No-code gate — Spec → Constraints → Quality Attribute Scenario → C4 → Architecture Decision Record → then code
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# No-code gate

Product crates, daemons, and extensions are **forbidden** until the checklist
in `CONTRIBUTING.md` is green. This tree is requirements, constraints, and
architecture analysis until then.

## Why (fail-modes if skipped)

| Skip | Fail-mode |
| --- | --- |
| C4 without Architecture Decision Records | Stale ownership sketches treated as Accepted |
| Latency adjectives without Architecture Tradeoff Analysis Method scenarios | Not a non-functional requirement |
| Polyglot without bounded-context nests | Fashion scaffolds, not product law |
| Formal labels without artifacts | Marketing — reject `proved` claims |

## Allowed before gate

- Requirements, constraints, Quality Attribute Scenario, Requirements
  Traceability Matrix  
- C4 models (Context / Container / Component)  
- Architecture Decision Records (Nygard)  
- Research memos and Architecture Tradeoff Analysis Method tradeoff tables  
- Doc linters / link checkers  

## Forbidden before gate

- Engine crates, daemons, gems, JVM services, WebAssembly binaries as product  
- “Just a spike folder” that becomes the tip without Architecture Decision
  Record Accept  
- Any Python product scaffolding / Spec server / ACI nest revival for this
  port — reject  

---
title: C4 modeling standard
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# C4 standard

| Level | What it binds | When required | If missing |
| --- | --- | --- | --- |
| **Context** | System + actors + external systems | Before any Implement | Block Implement |
| **Container** | Deployable/runtime unit per language nest | Before any Implement | Block Implement |
| **Component** | Major parts inside one container | Before coding that container | Block that container’s crates |
| **Code** | Classes/modules | **After** Component + Architecture Decision Records; optional | Leave deferred (Architecture Decision Record ADR-0008) |

Diagrams: Mermaid (or exported PNG) under `docs/c4/diagrams/`.  
Every container cites Architecture Decision Record IDs. A diagram edge without
an Architecture Decision Record citation is a sketch — not System of Record.

---
title: C4 modeling standard
status: ACTIVE
date: '2026-08-10'
---

# C4 standard

Levels used here:

| Level | Purpose | When required |
| --- | --- | --- |
| **Context** | System + actors + external systems | Before any Implement |
| **Container** | Deployable/runtime units (per language BC) | Before any Implement |
| **Component** | Major components inside a container | Before coding that container |
| **Code** | Classes/modules | **After** Component + ADRs; optional |

Diagrams are Mermaid (or exported PNG) under `docs/c4/diagrams/`.  
Every container maps to a polyglot BC and cites ADRs.

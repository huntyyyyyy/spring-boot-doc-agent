---
title: C4 Level 1 — System Context
status: DRAFT
date: '2026-08-10'
adr_refs:
  - Architecture Decision Record ADR-0001
---

# Context

## In one sentence

Verified Architecture Engine helps operators, architects, and developers get
**traceable** Spring wiring and architecture-lock answers for a target codebase.

## Actors and externals

```mermaid
C4Context
    title System Context — Verified Architecture Engine
    Person(op, "Agent operator", "Asks wiring/lock questions")
    Person(arch, "Architect", "Authors locks")
    Person(dev, "Developer", "Edits Java in IDE")
    Person(ci, "CI steward", "Merge gates")
    System(vae, "Verified Architecture Engine", "Polyglot local-first verify")
    System_Ext(repo, "Target Spring repo", "Java sources + build")
    System_Ext(scip, "scip-java", "Produces index.scip")
    System_Ext(ide, "IDE / Cursor", "LSP + panels")
    Rel(op, vae, "Queries / fitness_check")
    Rel(arch, vae, "Publishes locks (git)")
    Rel(dev, ide, "Edits")
    Rel(ide, vae, "Diagnostics")
    Rel(ci, vae, "Verify gate")
    Rel(vae, repo, "Reads sources")
    Rel(vae, scip, "Invokes / consumes index")
    Rel(vae, ide, "publishDiagnostics")
```

## Notes

- Target repo + locks (git) are System of Record inputs; indexes/registry are derived.
- large language model tools may assist remediation later; they are **not** context authorities.

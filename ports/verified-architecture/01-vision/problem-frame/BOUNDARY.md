---
title: Product boundary (draft)
status: DRAFT — awaits open question OQ-01 human Accept
date: '2026-08-10'
traces: open question OQ-01
---

# Product boundary

## One sentence

A **local developer tool** that builds a **virtual dependency/Dependency Injection graph** for a
target codebase, evaluates **git-versioned architectural locks**, and emits
**explainable proof-carrying receipts** — shared by humans and agents — preferring
**Unknown** over wrong answers.

## In

- Out-of-process command-line interface (+ later Language Server Protocol/Model Context Protocol) over a target git workspace
- Consume Source Code Index Protocol indexes + source ASTs; derived SQLite registry **and claim memory** written only by the **Rust** verify engine
- Policy locks in-repo; deterministic LockCheck
- Artifact-Anchored Verification Memory dispositions (`unprovable` > guess); Stateful Tool-Enabled Agentic Deployment-typed tool ids
- Retrieval-Augmented Generation over *this* planning corpus (and later assist text) **without** using it as verify System of Record

## Out (minimum viable product)

- Org-wide social knowledge-graph SaaS / Backstage mesh
- Embedding cosine as symbol or bean identity
- Claiming Spring runtime fidelity (`@Conditional`, AOP proxies) as proved
- Shipping nine-language monorepo as day-one identity
- **Python** verify/Specification corpus host (tombstone nest; Architecture Decision Record ADR-0001)

## Dual surfaces (explicit)

| Surface | Writes / owns | Must not |
| --- | --- | --- |
| **Verify engine** (**Rust**) | Graph edges, lock verdicts, freshness-bound receipts, claim dispositions | Treat chat or Retrieval-Augmented Generation text as witness |
| **Planning Retrieval-Augmented Generation corpus** | Progressive disclosure packs for agents/devs designing the engine | Serve as System of Record for binding or lock truth |

Shared repo hygiene only. Fail-mode: merging the two Systems of Record → open question OQ-02 reopen + reject codegen.

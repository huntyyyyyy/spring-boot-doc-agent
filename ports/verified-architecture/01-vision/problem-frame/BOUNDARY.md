---
title: Product boundary (draft)
status: DRAFT — awaits OQ-01 human Accept
date: '2026-08-10'
traces: OQ-01
---

# Product boundary

## One sentence

A **local developer tool** that builds a **virtual dependency/DI graph** for a
target codebase, evaluates **git-versioned architectural locks**, and emits
**explainable proof-tour receipts** — shared by humans and agents — preferring
**Unknown** over wrong answers.

## In

- Out-of-process CLI (+ later LSP/MCP) over a target git workspace
- Consume SCIP indexes + source ASTs; derived SQLite registry **and claim memory**
- Policy locks in-repo; deterministic LockCheck
- EA-Graph dispositions (`unprovable` > guess); STEAD-typed tool ids
- RAG over *this* planning corpus (and later assist text) **without** using it as verify SoR

## Out (MVP)

- Org-wide social knowledge-graph SaaS / Backstage mesh
- Embedding cosine as symbol or bean identity
- Claiming Spring runtime fidelity (`@Conditional`, AOP proxies) as proved
- Shipping nine-language monorepo as day-one identity

## Dual surfaces (explicit)

| Surface | Job |
| --- | --- |
| **Verify engine** | Graph + locks + receipts |
| **Planning RAG corpus** | Progressive disclosure for agents/devs designing the engine |

They share repo hygiene; they do **not** share SoR.

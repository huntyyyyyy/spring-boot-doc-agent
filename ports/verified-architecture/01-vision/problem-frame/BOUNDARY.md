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
**explainable proof-tour receipts** — shared by humans and agents — preferring
**Unknown** over wrong answers.

## In

- Out-of-process command-line interface (+ later Language Server Protocol/Model Context Protocol) over a target git workspace
- Consume Source Code Index Protocol indexes + source ASTs; derived SQLite registry **and claim memory**
- Policy locks in-repo; deterministic LockCheck
- EA-Graph dispositions (`unprovable` > guess); Stateful Tool-Enabled Agentic Deployment-typed tool ids
- Retrieval-Augmented Generation over *this* planning corpus (and later assist text) **without** using it as verify System of Record

## Out (minimum viable product)

- Org-wide social knowledge-graph SaaS / Backstage mesh
- Embedding cosine as symbol or bean identity
- Claiming Spring runtime fidelity (`@Conditional`, AOP proxies) as proved
- Shipping nine-language monorepo as day-one identity

## Dual surfaces (explicit)

| Surface | Job |
| --- | --- |
| **Verify engine** | Graph + locks + receipts |
| **Planning Retrieval-Augmented Generation corpus** | Progressive disclosure for agents/devs designing the engine |

They share repo hygiene; they do **not** share System of Record.

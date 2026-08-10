---
title: StRS — Stakeholder Requirements Specification
status: DRAFT — awaiting stakeholder review
date: '2026-08-10'
standard: ISO/IEC/IEEE 29148-shaped
---

# StRS — Stakeholder requirements

## Purpose

Define what the Verified Architecture Engine must achieve for stakeholders,
**without** binding implementation language. SRS and C4 derive from this.

## Actors

| ID | Actor | Core concern |
| --- | --- | --- |
| **A-OP** | Agent / tool operator | Ask wiring/architecture questions without hallucinated beans |
| **A-ARCH** | Architect | Author locks once; humans + AI share enforcement |
| **A-DEV** | Developer (IDE) | Same violation signal as the agent path |
| **A-CI** | CI / merge steward | Deterministic gate; single oracle writer |
| **A-OWN** | Target-repo owner | Bounded index cost; Unknown preferred over wrong |

## Mission need

Operators and architects need **answers about Spring wiring and architecture
policy** that are **traceable to index + locks**, not chat invention.

**Measurable intent (v1):** resolve an injection/type to an implementation **or**
explicit `Unknown`, with a **proof-tour receipt** of witness IDs; never silently
pick among ambiguous candidates.

## Goals

| ID | Goal |
| --- | --- |
| G1 | Virtual Spring/dep graph + lock checks on realistic plants |
| G2 | Same lock policy for agent and human paths |
| G3 | Explainable verify (receipt cites lock + graph witnesses) |

## Out of scope (this wave)

- Full JVM fidelity (`@Conditional`, AOP proxies, SpEL) as “proved”
- Embeddings/RAG as authority for bindings
- Org-wide social knowledge-graph SaaS as Must
- Mesh / Backstage as merge SoT

## Polyglot product identity

The system is delivered as a **polyglot** monorepo of first-class language BCs
(Rust engine, WASM trust boundary, Go chassis, Ruby locks, Clojure graph brain,
SQLite registry, TS IDE/MCP, Python as **peer** ACI — not majority kernel).
See ADR-0001.

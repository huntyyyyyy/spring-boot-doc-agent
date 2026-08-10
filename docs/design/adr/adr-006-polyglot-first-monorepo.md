---
title: 'ADR-006: Polyglot-first monorepo (Rust WASM Go Ruby Clojure SQLite TS C Zig)'
status: Proposed
date: '2026-08-10'
adr: ADR-006
related:
  - docs/design/adr/README.md
  - docs/research/process/55-e-lie0-full-polyglot-product-portfolio-2026-08-10.md
  - docs/design/adr/adr-005-python-tip-oracle-writer.md
  - docs/research/process/54-e-lie0-atam-qas-adr-formal-boundaries-2026-08-10.md
claim_tiers: Confirmed
last_reviewed: '2026-08-10'
---

# ADR-006: Polyglot-first monorepo

## Context

Stakeholders directed that E-LIE0 is a **full** polyglot product — Rust, WASM
and WASM/Rust toolkits, SQLite, Go, Ruby, Clojure, Python, TypeScript as needed,
C when necessary, Zig when earned — not a Python core with demoted sidecars.
Prior agent memos over-weighted “Python tip identity.” Oracle single-writer and
ATAM/QAS gates remain necessary for shippability.

## Decision

We will treat the **monorepo as polyglot-first**: first-class BCs for Rust
engine, WASM guests/hosts, Go daemon, Ruby lock tooling, Clojure graph brain,
SQLite registry, Python ACI/oracle (transitional), TypeScript IDE/MCP, plus C/Zig
Spikes when required. ADR-005 remains the **current** oracle-writer constraint
until an explicit cutover ADR supersedes it — it does **not** define product
identity.

## Status

Proposed (awaiting stakeholder Accept — aligned with stated direction).

## Consequences

Positive: matches user vision; unlocks rich feature set; clear language ownership.  
Negative: wider CI matrix; supply-chain surface; more Spike discipline required.  
Rejected: “Python-only Pilot forever”; forbidding Ruby/Clojure/Go/Rust in-tree;
greenfield abandon of this repo’s plants.

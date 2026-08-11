---
title: Architecture Decision Records — index (stack-aligned)
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Records

Nygard records live here. Rows stay **Proposed** until a human Accepts.
**Stack lock (2026-08-11):** only Rust may write engine effects and Spec corpus
Model Context Protocol indexes; TypeScript may present IDE surfaces only;
**Refuse Python** runtime for this port; WebAssembly LockCheck guest =
**Could / Wave-3** — never Spec host. FREEZE: deepen receipt β/ρ, claim
withdrawal, handle lifecycle only — new matrices without human override =
reject.

| ID | Bound choice | Nest / locus | Align |
| --- | --- | --- | --- |
| [0001](adr-0001-polyglot-first-product.md) | One Accepted language → one bounded context; **Refuse Python** | nests (08 tombstone) | Amended |
| [0002](adr-0002-sqlite-registry.md) | Bean/edge rows via rusqlite only | `02-registry-sqlite` | OK |
| [0003](adr-0003-packwerk-lock-ir.md) | Shared lock Intermediate Representation; Ruby authors | `03-locks-ruby` | OK |
| [0004](adr-0004-native-then-wasm-lockcheck.md) | Native LockCheck Must; WebAssembly guest **Could**/Wave-3 | `01` + `06` | Amended |
| [0005](adr-0005-clojure-graph-brain.md) | Datascript over EDN export; not merge oracle | `05-graph-clojure` | OK |
| [0006](adr-0006-single-oracle-writer.md) | ≤1 gate writer; hypothesis **Rust** | ADR-0007 | Amended |
| [0007](adr-0007-rust-owns-engine.md) | Rust engine **and** Spec corpus Model Context Protocol host | `01-engine-rust` | Amended |
| [0008](adr-0008-c4-before-code.md) | Context+Container+Architecture Decision Records before crates | `docs/c4/`, gate | OK |
| [0009](adr-0009-go-chassis-daemon.md) | Go watches/reindexes; never oracle writer | `04-chassis-go` | OK |
| [0010](adr-0010-typescript-ide-mcp.md) | TypeScript presentation Model Context Protocol only | `07-ide-typescript` | Amended |
| [0011](adr-0011-mcp-protocol-and-tool-surface.md) | Pin `2026-07-28`; verify ≠ Spec corpus surfaces | Interface Control Document + Spike | Amended |

Filled matrices: `07-system-design/decisions/` (Draft / FREEZE). Adding a new
matrix file without human override fails FREEZE.

**Requirements / C4 System of Record:** `03-requirements/` and `docs/c4/`.
Flat `docs/requirements/` are pointers only. Confidence sketch:
`07-system-design/c4/C4-BRIEF-CONFIDENCE.md`.

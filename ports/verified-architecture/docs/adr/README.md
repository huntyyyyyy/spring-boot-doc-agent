---
title: Architecture Decision Records — index (stack-aligned)
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Records

Nygard format. All rows are **Proposed** (human Accept pending) unless noted.
**Stack lock (2026-08-11):** Rust engine + Spec corpus Model Context Protocol;
TypeScript IDE presentation; **Refuse Python**; WebAssembly = LockCheck guest
Could — not Spec host.

| ID | Decision (one line) | Nest / locus | Align |
| --- | --- | --- | --- |
| [0001](adr-0001-polyglot-first-product.md) | Polyglot peers; **Refuse Python** | nests (08 tombstone) | Amended |
| [0002](adr-0002-sqlite-registry.md) | SQLite derived registry via Rust | `02-registry-sqlite` | OK |
| [0003](adr-0003-packwerk-lock-ir.md) | Packwerk-shaped lock IR; Ruby DX | `03-locks-ruby` | OK |
| [0004](adr-0004-native-then-wasm-lockcheck.md) | Native LockCheck first; WASM guest Pilot | `01` + `06` | OK |
| [0005](adr-0005-clojure-graph-brain.md) | Clojure/bb Datascript over EDN export | `05-graph-clojure` | OK |
| [0006](adr-0006-single-oracle-writer.md) | Single gate writer; hypothesis **Rust** | ADR-0007 | Amended |
| [0007](adr-0007-rust-owns-engine.md) | Rust owns engine **and** Spec corpus MCP | `01-engine-rust` | Amended |
| [0008](adr-0008-c4-before-code.md) | C4 + ADRs before product code | `docs/c4/`, gate | OK |
| [0009](adr-0009-go-chassis-daemon.md) | Go watch/reindex chassis | `04-chassis-go` | OK |
| [0010](adr-0010-typescript-ide-mcp.md) | TS owns IDE / **presentation** MCP only | `07-ide-typescript` | Amended |
| [0011](adr-0011-mcp-protocol-and-tool-surface.md) | Pin `2026-07-28`; dual surfaces (verify vs Spec) | ICD + Spike | Amended |

Decision matrices (Draft / FREEZE): `07-system-design/decisions/` — do not add
new matrices without human override.

**Requirements / C4 SoT:** prefer `03-requirements/` and `docs/c4/` (Nygard C4
levels). Flat `docs/requirements/` are **pointers**. Brief confidence sketch:
`07-system-design/c4/C4-BRIEF-CONFIDENCE.md`.

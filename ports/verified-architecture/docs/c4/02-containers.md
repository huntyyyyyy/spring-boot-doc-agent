---
title: C4 Level 2 — Containers (polyglot bounded contexts)
status: DRAFT
date: '2026-08-10'
last_reviewed: '2026-08-11'
adr_refs:
  - Architecture Decision Record ADR-0001
  - Architecture Decision Record ADR-0002
  - Architecture Decision Record ADR-0003
  - Architecture Decision Record ADR-0004
  - Architecture Decision Record ADR-0005
  - Architecture Decision Record ADR-0006
  - Architecture Decision Record ADR-0007
  - Architecture Decision Record ADR-0009
  - Architecture Decision Record ADR-0010
---

# Containers

One deployable/runtime unit per Accepted language (Architecture Decision
Record ADR-0001). **No Python container** — Refuse; nest 08 tombstoned;
revival = reject.

```mermaid
C4Container
    title Containers — polyglot BCs
    Person(user, "Operator / Dev / CI")
    Container(engine, "Engine", "Rust", "SCIP decode, resolve, LockCheck, receipts, wasmtime host")
    ContainerDb(reg, "Registry", "SQLite", "Derived beans/edges")
    Container(wasm, "Lock guest", "WASM", "Capability-sandboxed LockCheck")
    Container(daemon, "Chassis daemon", "Go", "Watch, reindex, stamps")
    Container(locks, "Lock DX", "Ruby", "Packwerk-shaped manifests / todo")
    Container(brain, "Graph brain", "Clojure/bb", "Datascript queries over EDN")
    Container(ide, "IDE / MCP UI", "TypeScript", "Diagnostics + panels")
    Container_Ext(plant, "Target repo + scip-java", "Java", "Sources + index.scip")
    Rel(user, ide, "Edits / asks")
    Rel(user, engine, "CLI / MCP tools")
    Rel(daemon, plant, "Watches")
    Rel(daemon, engine, "Triggers index/verify")
    Rel(engine, plant, "Reads index/sources")
    Rel(engine, reg, "R/W derived facts")
    Rel(engine, wasm, "Optional LockCheck")
    Rel(locks, engine, "Lock IR")
    Rel(engine, brain, "EDN export")
    Rel(ide, engine, "LSP / MCP")
```

| Container | Language | Bound / fail-mode |
| --- | --- | --- |
| Engine | Rust | ADR-0007, ADR-0004 — sole oracle / Spec corpus Model Context Protocol host |
| Registry | SQLite | ADR-0002 — rusqlite writers only |
| Lock guest | WebAssembly | ADR-0004 — **Could / Wave-3**, not Must, not Spec host |
| Chassis | Go | ADR-0009 — triggers only; never oracle writer |
| Lock DX | Ruby | ADR-0003 — authors Intermediate Representation |
| Graph brain | Clojure | ADR-0005 — EDN read-mostly |
| IDE / Model Context Protocol UI | TypeScript | ADR-0010 — **presentation only** |
| Spec corpus Model Context Protocol | Rust | ADR-0007 + Spike — not TypeScript |
| C / Zig shims | C/Zig | earned Spikes only |
| ~~Optional ACI glue~~ | ~~Python~~ | **Refuse** — nest 08 tombstoned |

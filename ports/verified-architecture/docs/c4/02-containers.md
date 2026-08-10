---
title: C4 Level 2 — Containers (polyglot BCs)
status: DRAFT
date: '2026-08-10'
adr_refs:
  - ADR-0001
  - ADR-0002
  - ADR-0003
  - ADR-0004
  - ADR-0005
  - ADR-0006
  - ADR-0007
  - ADR-0009
  - ADR-0010
---

# Containers

Each container is a **first-class language BC** (ADR-0001). Python is optional
peer glue — not shown as the hub.

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

| Container | Language | ADR |
| --- | --- | --- |
| Engine | Rust | 0007, 0004 |
| Registry | SQLite | 0002 |
| Lock guest | WASM | 0004 |
| Chassis | Go | 0009 |
| Lock DX | Ruby | 0003 |
| Graph brain | Clojure | 0005 |
| IDE/MCP | TypeScript | 0010 |
| Optional ACI glue | Python | peer only — not required hub |
| C / Zig shims | C/Zig | earned Spikes |

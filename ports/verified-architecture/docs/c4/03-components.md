---
title: C4 Level 3 — Engine components (Rust)
status: DRAFT
date: '2026-08-10'
last_reviewed: '2026-08-11'
adr_refs:
  - Architecture Decision Record ADR-0007
  - Architecture Decision Record ADR-0002
  - Architecture Decision Record ADR-0004
---

# Components — Engine (Rust)

Rust engine internals only. Other containers lack Component diagrams until
their Implement wave — do not invent Component ownership from this file.

```mermaid
C4Component
    title Engine components
    Container_Boundary(engine, "Engine (Rust)") {
        Component(index, "IndexPort", "Rust", "Load/validate index.scip digests")
        Component(facts, "SymbolFact", "Rust", "Normalized symbols")
        Component(reg, "RegistrySql", "Rust", "SQLite schema writers")
        Component(resolve, "WiringResolver", "Rust", "Bind or Unknown")
        Component(lockir, "LockIR", "Rust", "Parse Packwerk-shaped IR")
        Component(lockchk, "LockCheck", "Rust", "Evaluate locks vs edges")
        Component(receipt, "Receipt", "Rust", "Proof-carrying JSON")
        Component(host, "WasmHost", "Rust", "wasmtime embedder")
        Component(export, "EdnExport", "Rust", "Export for Clojure BC")
    }
    Rel(index, facts, "Yields")
    Rel(facts, reg, "Persists")
    Rel(reg, resolve, "Candidates")
    Rel(resolve, lockchk, "Edges")
    Rel(lockir, lockchk, "Rules")
    Rel(lockchk, receipt, "Witnesses")
    Rel(lockchk, host, "Optional guest")
    Rel(reg, export, "Snapshot")
```

`WasmHost` → guest LockCheck remains **Could / Wave-3** (Architecture Decision
Record ADR-0004); treat the Rel as optional until Wave-3 earns it.

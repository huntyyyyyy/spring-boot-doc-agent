---
title: Polyglot portfolio (planning view)
status: DRAFT
date: '2026-08-10'
---

# Polyglot portfolio

Product identity (Architecture Decision Record ADR-0001). Detailed toolkits planned; **no code yet**.

| bounded context | Language | Owns | Architecture Decision Record |
| --- | --- | --- | --- |
| Engine | Rust | Resolve, LockCheck, receipts, wasmtime host | 0007, 0004 |
| Registry | SQLite | Derived beans/edges | 0002 |
| Lock guest | WebAssembly | Sandboxed checks | 0004 |
| Chassis | Go | Watch/reindex | 0009 |
| Lock DX | Ruby | Packwerk-shaped manifests | 0003 |
| Graph brain | Clojure | Datascript/Datalog | 0005 |
| IDE/Model Context Protocol | TypeScript | Presentation | 0010 |
| ACI glue | Python | Optional peer only | — |
| Native shims | C | Grammars / amalgamation when needed | Spike |
| Systems alt | Zig | Earned Spike | Spike |

Future layout (post-gate): `crates/`, `go/`, `ruby/`, `clj/`, `wasm/`, `extensions/`, …

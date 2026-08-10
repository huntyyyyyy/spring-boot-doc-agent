---
title: Ports and adapters (language-agnostic)
status: DRAFT
date: '2026-08-10'
---

# Ports

Implementations may be Rust/Go/… later; **ports are stable names** for ICDs.

| Port | Responsibility | MVP |
| --- | --- | --- |
| `IndexReader` | Load SCIP (+ optional CST hints) | Must |
| `AnnotationScan` | Discover candidate beans/components from source | Must |
| `Registry` | Persist nodes/edges (SQLite) | Must |
| `Resolver` | injection_point → bean \| Unknown | Must |
| `LockCheck` | Evaluate lock IR against graph | Must |
| `ReceiptWriter` | Emit proof-tour steps | Must |
| `Watch` | FS events → reindex dirty set | Should (Go Pilot) |
| `GraphQuery` | Ad-hoc Datalog/EDN queries | Could (bb Pilot) |
| `Sandbox` | Run LockCheck guest under WASM caps | Could |
| `LspDiagnostics` | publishDiagnostics | Should (Wave-2) |
| `RemediationAssist` | RAG/LLM suggestions | Could — non-witness |

## Anti-god rule

No single module owns Index+Resolve+Lock+LSP+RAG. Compose via these ports.

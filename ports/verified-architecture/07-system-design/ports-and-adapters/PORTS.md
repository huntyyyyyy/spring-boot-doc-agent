---
title: Ports and adapters (language-agnostic)
status: DRAFT
date: '2026-08-10'
---

# Ports

Implementations may be Rust/Go/… later; **ports are stable names** for ICDs.

| Port | Responsibility | minimum viable product |
| --- | --- | --- |
| `IndexReader` | Load Source Code Index Protocol (+ optional CST hints) | Must |
| `AnnotationScan` | Discover candidate beans/components from source | Must |
| `Registry` | Persist nodes/edges (SQLite) | Must |
| `Resolver` | injection_point → bean \| Unknown | Must |
| `LockCheck` | Evaluate lock IR against graph | Must |
| `ReceiptWriter` | Emit proof-tour steps | Must |
| `ClaimMemory` | EA-Graph anchors + withdraw dispositions | Must |
| `Watch` | FS events → reindex dirty set | Should (Go Pilot) |
| `GraphQuery` | Ad-hoc Datalog/EDN queries | Could (bb Pilot) |
| `Sandbox` | Run LockCheck guest under WebAssembly caps | Could |
| `LspDiagnostics` | publishDiagnostics | Should (Wave-2) |
| `RemediationAssist` | Retrieval-Augmented Generation/large language model suggestions | Could — non-witness |
| `AgentMemory` | Episodic/entity memory for agents | Could — **≠** Registry/ClaimMemory |
| `EquivarianceWrap` | Canonicalize tool args (Stateful Tool-Enabled Agentic Deployment) | Spike → Should before FO claims |

## Anti-god rule

No single module owns Index+Resolve+Lock+Language Server Protocol+Retrieval-Augmented Generation+Memory. Compose via these ports.

## Jul–Aug 2026 amendment

Split verify registry from agent memory (`research/adversarial/july-august-2026-overturn-review.md` A4).
Aria-shaped loop: agent proposes → `LockCheck`+`ReceiptWriter` harness decides.
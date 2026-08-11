---
title: Ports and adapters (language-agnostic)
status: DRAFT
date: '2026-08-10'
---

# Ports

Stable names bound to Interface Control Documents. **Rust** alone may write
oracle artifacts and Spec-corpus indexes (engine Pilot after ports).
**TypeScript** may only present (Model Context Protocol / Language Server
Protocol). **Refuse Python** for this port’s host/engine. **WebAssembly**
LockCheck guest = **Could** / Wave-3 — isolation ≠ proof.

| Port | Responsibility | minimum viable product |
| --- | --- | --- |
| `IndexReader` | Load Source Code Index Protocol (+ optional Concrete Syntax Tree hints) | Must |
| `AnnotationScan` | Discover candidate beans/components from source | Must |
| `Registry` | Persist nodes/edges (SQLite) | Must |
| `Resolver` | injection_point → bean \| Unknown | Must |
| `LockCheck` | Evaluate lock Intermediate Representation against graph | Must |
| `ReceiptWriter` | Emit proof-tour steps | Must |
| `ClaimMemory` | Artifact-anchored claims + withdraw dispositions | Must |
| `Watch` | Filesystem events → reindex dirty set | Should (Go Pilot) |
| `GraphQuery` | Ad-hoc Datalog/EDN queries | Could (Babashka Pilot) |
| `Sandbox` | Run LockCheck guest under WebAssembly caps | Could |
| `LspDiagnostics` | publishDiagnostics | Should (Wave-2) |
| `RemediationAssist` | Retrieval-Augmented Generation / large language model suggestions | Could — non-witness |
| `AgentMemory` | Episodic/entity memory for agents | Could — **≠** Registry / ClaimMemory |
| `EquivarianceWrap` | Canonicalize tool args (Stateful Tool-Enabled Agentic Deployment) | Spike → Should before FO claims |

## Anti-god rule

No single module owns Index + Resolve + Lock + Language Server Protocol +
Retrieval-Augmented Generation + Memory. Compose via these ports; violation =
reject the change.

## Jul–Aug 2026 amendment

Split verify registry from agent memory
(`research/adversarial/july-august-2026-overturn-review.md` A4). Aria-shaped
loop: agent proposes → `LockCheck` + `ReceiptWriter` harness decides.

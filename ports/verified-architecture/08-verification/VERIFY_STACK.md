---
title: Verify stack — graph + locks and claim memory and tool constraints
status: DRAFT
date: '2026-08-10'
sources:
  - arXiv:2608.04278  # Artifact-Anchored Verification Memory (EA-Graph)
  - arXiv:2608.03609  # Stateful Tool-Enabled Agentic Deployments
  - arXiv:2607.06341  # Aria harness pattern
---

# Verify stack (Must spine — amended)

**Do not cling to “graph + locks” alone.** Wave-1 verify is four coupled layers.
Skipping artifact-anchored claim memory or Stateful Tool-Enabled Agentic
Deployment tool constraints recreates the attacks we already lost.

Whole words in prose — see root `GLOSSARY.md`.

```text
                    ┌─────────────────────────────────────┐
                    │  Agent / Human proposes change       │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
┌──────────────┐   L1    ┌──────────────┐   L2    ┌──────────────┐
│ Index / SCIP │────────▶│ Graph/Registry│────────▶│ LockCheck    │
│ + CST hints  │         │ (derived)     │         │ (policy       │
│              │         │               │         │  System of    │
│              │         │               │         │  Record)      │
└──────────────┘         └───────┬───────┘         └───────┬──────┘
                                 │                         │
                                 │    anchors + digests      │
                                 ▼                         ▼
                    ┌─────────────────────────────────────┐
                    │  Artifact-anchored claim memory (L2b) │
                    │  evidence independent of freshness    │
                    │  disposition: unaffected|affected|    │
                    │               unprovable              │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  Receipt / proof-carrying writer      │
                    │  (witnesses exclude large language    │
                    │   model / retrieval text)             │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │  Stateful Tool-Enabled Agentic       │
                    │  Deployment constraints on tools     │
                    │  (equivariance / canonical ids)      │
                    │  before First-Order Computation Tree │
                    │  Logic-like claims                   │
                    └─────────────────────────────────────┘
```

## Layer contracts

| Layer | Job | System of Record class | July–August driver |
| --- | --- | --- | --- |
| **L1 Navigate** | Symbols / Concrete Syntax Tree → candidates | Index System of Record (Source Code Index Protocol) + derived scan | — |
| **L2 Policy** | Locks on graph | Policy System of Record (git locks) | Packwerk pattern |
| **L2b Claims** | Persist *verification claims* anchored to content digests; withdraw on drift | Claim store (derived, rebuildable) | *EA-Graph: Artifact-Anchored Verification Memory* (2608.04278) |
| **L3 Proof** | Optional Satisfiability Modulo Theories / Kani / WebAssembly | Proof System of Record for encoded properties only | Aria / VeriSynth patterns — not minimum viable product Must |
| **Tool boundary** | Model Context Protocol / command-line interface arguments equivariant under identifier rename | Interface constraint | *Formal Verification of Agentic Systems over Operational Data* (2608.03609) |

## Hard rules (addressing the attacks)

### Artifact-anchored claim memory (must implement in specification → then code)

1. Every lock/resolve outcome that becomes a **claim** stores `anchor_digest`
   of the content used to establish it.
2. **Evidence strength** and **freshness** are independent fields.
3. On upstream drift, disposition is `unaffected` | `affected` | **`unprovable`**.
4. **`unprovable` never becomes a guessed bean/edge.** Same severity as Unknown.
5. Loss of proof does not delete the last verified artifact record (audit keep).

Schemas: `receipts/receipt-schema-draft.md`, `claim-memory/EA_GRAPH_CLAIMS.md`.

### Stateful Tool-Enabled Agentic Deployment constraints (must constrain tools even if we never run First-Order Computation Tree Logic)

1. Do **not** claim “the agent + Model Context Protocol system satisfies business
   First-Order Computation Tree Logic” without a finite-domain + equivariance
   story (undecidable in general).
2. Tool arguments that carry opaque identifiers (bean id, path, symbol, edge id)
   must be **renamed consistently** when the underlying data is α-renamed — or
   wrap calls in a canonicalizer (`EquivarianceWrap` port).
3. Minimum viable product may **defer First-Order Computation Tree Logic model
   checking** but **must not** design Model Context Protocol schemas that bake
   in non-equivariant agent whims (stringly identifiers from large language
   model free text).
4. Spike: `12-delivery/spike-charters/SPIKE-STEAD-equivariance.md`.

### Aria-shaped harness (process)

Agent / large language model **proposes**. `LockCheck` + claim memory + receipt
writer **decide**. Kernel/harness is the trust anchor — never the model.

### Graph + locks (still necessary — not sufficient)

Cycles, layer rules, resolve→Unknown remain the cheap structural core.
They are **inputs** to claim memory, not a substitute for it.

## What “done” looks like for Wave 1

Command-line interface verify that:

1. Builds/updates graph registry  
2. Evaluates locks  
3. Writes receipts **and** claim records with digests  
4. On re-run after file edit: marks prior claims affected/unprovable correctly  
5. Exposes tools whose identifiers come from registry / Source Code Index Protocol — not raw large language model strings  

Full First-Order Computation Tree Logic checker for Stateful Tool-Enabled
Agentic Deployments = Wave 4 research — constraints on schemas = **Wave 0 /
Wave 1**.

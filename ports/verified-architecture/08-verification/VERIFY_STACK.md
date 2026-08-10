---
title: Verify stack — graph + locks ∧ EA-Graph ∧ STEAD (not graph alone)
status: DRAFT
date: '2026-08-10'
sources:
  - arXiv:2608.04278  # EA-Graph
  - arXiv:2608.03609  # STEAD
  - arXiv:2607.06341  # Aria harness pattern
---

# Verify stack (Must spine — amended)

**Do not cling to “graph + locks” alone.** Wave-1 verify is four coupled layers.
Skipping EA-Graph or STEAD constraints recreates the attacks we already lost.

```text
                    ┌─────────────────────────────────────┐
                    │  Agent / Human proposes change       │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
┌──────────────┐   L1    ┌──────────────┐   L2    ┌──────────────┐
│ Index/SCIP   │────────▶│ Graph/Registry│────────▶│ LockCheck    │
│ + CST hints  │         │ (derived)     │         │ (policy SoR) │
└──────────────┘         └───────┬───────┘         └───────┬──────┘
                                 │                         │
                                 │    anchors + digests      │
                                 ▼                         ▼
                    ┌─────────────────────────────────────┐
                    │  EA-Graph claim memory (L2b)          │
                    │  evidence ⊥ freshness                 │
                    │  disposition: unaffected|affected|    │
                    │               unprovable              │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  Receipt / proof-tour writer          │
                    │  (witnesses exclude LLM/RAG text)     │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────▼───────────────────┐
                    │  STEAD constraints on tool surface   │
                    │  (equivariance / canonical ids)      │
                    │  before FO-CTL-like claims           │
                    └─────────────────────────────────────┘
```

## Layer contracts

| Layer | Job | SoR class | Jul–Aug driver |
| --- | --- | --- | --- |
| **L1 Navigate** | Symbols/CST → candidates | Index SoR (SCIP) + derived scan | — |
| **L2 Policy** | Locks on graph | Policy SoR (git locks) | Packwerk pattern |
| **L2b Claims** | Persist *verification claims* anchored to content digests; withdraw on drift | Claim store (derived, rebuildable) | **EA-Graph 2608.04278** |
| **L3 Proof** | Optional SMT/Kani/WASM | Proof SoR for encoded props only | Aria/VeriSynth patterns — not MVP Must |
| **Tool boundary** | MCP/CLI args equivariant under id rename | Interface constraint | **STEAD 2608.03609** |

## Hard rules (addressing the attacks)

### EA-Graph (must implement in Spec → then code)

1. Every lock/resolve outcome that becomes a **claim** stores `anchor_digest`
   of the content used to establish it.
2. **Evidence strength** and **freshness** are independent fields.
3. On upstream drift, disposition is `unaffected` | `affected` | **`unprovable`**.
4. **`unprovable` never becomes a guessed bean/edge.** Same severity as Unknown.
5. Loss of proof does not delete the last verified artifact record (audit keep).

Schemas: `receipts/receipt-schema-draft.md`, `claim-memory/EA_GRAPH_CLAIMS.md`.

### STEAD (must constrain tools even if we never run FO-CTL)

1. Do **not** claim “the agent+MCP system satisfies business FO-CTL” without a
   finite-domain + equivariance story (undecidable in general).
2. Tool arguments that carry opaque ids (bean id, path, symbol, edge id) must
   be **renamed consistently** when the underlying data is α-renamed — or wrap
   calls in a canonicalizer (`EquivarianceWrap` port).
3. MVP may **defer FO-CTL model checking** but **must not** design MCP schemas
   that bake in non-equivariant agent whims (stringly ids from LLM free text).
4. Spike: `12-delivery/spike-charters/SPIKE-STEAD-equivariance.md`.

### Aria-shaped harness (process)

Agent/LLM **proposes**. `LockCheck` + claim memory + receipt writer **decide**.
Kernel/harness is the trust anchor — never the model.

### Graph + locks (still necessary — not sufficient)

Cycles, layer rules, resolve→Unknown remain the cheap structural core.
They are **inputs** to claim memory, not a substitute for it.

## What “done” looks like for W1

CLI verify that:

1. Builds/updates graph registry  
2. Evaluates locks  
3. Writes receipts **and** claim records with digests  
4. On re-run after file edit: marks prior claims affected/unprovable correctly  
5. Exposes tools whose ids come from registry/SCIP — not raw LLM strings  

STEAD full FO-CTL checker = W4 research — constraints on schemas = **W0/W1**.

---
title: Verify stack — graph + locks and claim memory and tool constraints
status: DRAFT
date: '2026-08-10'
sources:
  - arXiv:2608.04278  # Artifact-Anchored Verification Memory (EA-Graph)
  - arXiv:2608.03609  # Stateful Tool-Enabled Agentic Deployments
  - arXiv:2607.06341  # Aria harness pattern
---

# Verify stack (Must-intent spine — Pilot invent until Accept)

Wave-1 verify targets **four legs**. Exact public engines for L2b / STEAD wrap /
Proof-or-Stop product = **0** today → treat as **Must intent / Pilot invent**,
not industry Adopt. Skip L2b or tool boundary → recreate Jul–Aug attacks.
Whole words — root `GLOSSARY.md`.

```text
 Agent/Human proposes
        │
        ▼
 L1 Index/SCIP + CST ──▶ L2 Graph/Registry (derived) ──▶ L2 LockCheck (policy SoR)
                              │                              │
                              └──── anchors + digests ───────┘
                                        │
                                        ▼
                         L2b Artifact-anchored claim memory
                         evidence ⊥ freshness
                         disposition: unaffected|affected|unprovable
                                        │
                                        ▼
                         Receipt writer (witnesses exclude LLM/RAG text)
                                        │
                                        ▼
                         Tool boundary (STEAD): equivariant / canonical ids
                         before any FO-CTL-like claim
```

## Four Must-intent legs (Pilot invent until Accept)

| Leg | Job | SoR class | Fail-mode if skipped |
| --- | --- | --- | --- |
| **L1 Navigate** | Symbols/CST → candidates | Index SoR (SCIP) + derived scan | Soft resolve without index |
| **L2 Policy** | Locks on graph | Policy SoR (git locks) | Cycles/layers unchecked |
| **L2b Claims** | Persist claims on content digests; withdraw on drift | Claim store (derived) | Stale “green” after edit |
| **Tool boundary** | MCP/CLI args equivariant under id rename | Interface constraint | Hallucinated handles accepted |

Optional **L3 Proof** (SMT/Kani/WASM) = Wave-4 Could — not MVP Must.

## Hard rules

### L2b claim memory (spec → then code)

1. Claim stores `anchor_digest` of establishing content.
2. Evidence strength ⊥ freshness (independent fields).
3. Drift → `unaffected` | `affected` | **`unprovable`**.
4. **`unprovable` never becomes a guessed bean/edge** (same severity as Unknown).
5. Loss of proof keeps last verified artifact record (audit).

Schemas: `07-system-design/icd/receipt.schema.json` (SoT), `claim-memory/EA_GRAPH_CLAIMS.md`.
Historical sketch only: `receipts/receipt-schema-draft.md` (pointer — do not edit as SoT).

### STEAD tool constraints (even without FO-CTL checker)

1. No “agent+MCP satisfies business FO-CTL” without finite-domain + equivariance.
2. Opaque ids (bean/path/symbol/edge) rename consistently — or `EquivarianceWrap`.
3. MVP may defer FO-CTL checking; **must not** bake non-equivariant free-text ids into MCP schemas.
4. Spike: `12-delivery/spike-charters/SPIKE-STEAD-equivariance.md`.

### Aria harness

Model **proposes**. `LockCheck` + claim memory + receipt writer **decide**.
Kernel is trust anchor — never the model.

### Graph + locks

Necessary inputs to claim memory — **not** a substitute for L2b.

## Wave-1 done (predicate)

CLI verify that: (1) builds/updates registry, (2) evaluates locks, (3) writes
receipts **and** claim records with digests, (4) after file edit marks prior
claims affected/unprovable, (5) tools take registry/SCIP ids — not raw LLM
strings. Full FO-CTL checker = Wave 4; schema constraints = Wave 0/1.

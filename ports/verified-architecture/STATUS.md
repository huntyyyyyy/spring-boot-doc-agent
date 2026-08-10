---
title: STATUS — single pointer for cold agents
status: ACTIVE
last_reviewed: '2026-08-10'
---

# STATUS

## Phase

**Spec / gap-fill** — **Implement = Refuse.**

## Must spine (amended — do not shrink)

Graph + locks **∧** EA-Graph claim memory **∧** STEAD tool constraints **∧**
receipts. Canonical: `08-verification/VERIFY_STACK.md`.

## Product one-liner (draft)

Local developer tool: virtual dep/DI graph, git locks, **anchored verification
claims** (unprovable > guess), receipts; agents propose / harness decides.
Boundary: `01-vision/problem-frame/BOUNDARY.md`.

## Next tasks (do in order)

1. Read `AGENT_WALKTHROUGH.md` + `STRUCTURE.md` if new to the tree
2. **Human Accept** VERIFY_STACK + BOUNDARY (or amend)
3. Promote ICD stubs: claim-memory API + MCP tools citing STEAD ST-1…5
   (`07-system-design/icd/`)
4. Write Must QAS files (`03-requirements/qas/`)
5. Close OQ-02…05 against SoR + receipts + Unknown taxonomy
6. Complete STEAD spike notes (even if FO-CTL deferred)
7. Human **W0 Approve** when DoR moves

## Do not do next

- Shrink spine back to “just graph+locks”
- Cargo / nine-language scaffolds
- MCP tools that take free-text entity names from the model
- Kuzu/Lance/Phi as verify SoR

## Gate refs

`AGENT_BOOTSTRAP` · `AGENT_WALKTHROUGH` · `STRUCTURE` · `VERIFY_STACK` ·
`claim-memory/EA_GRAPH_CLAIMS` · `stead/STEAD_CONSTRAINTS` · DoR · no-code-gate

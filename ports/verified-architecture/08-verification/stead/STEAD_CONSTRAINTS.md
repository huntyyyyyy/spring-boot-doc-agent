---
title: STEAD tool-boundary constraints — Spec (adopt 2608.03609 lessons)
status: DRAFT
date: '2026-08-10'
arxiv: '2608.03609'
---

# STEAD constraints (product Spec)

We **do not** implement FO-CTL model checking in MVP. We **do** adopt the
paper’s warning: LLM+tools over relational/operational data is easy to get
*formally* wrong. Design the tool surface so we don’t paint into that corner.

## Adopted constraints (W0/W1)

| ID | Constraint |
| --- | --- |
| **ST-1** | Tool parameters that name entities (bean, symbol, edge, path, claim) MUST be typed ids from Registry/SCIP/claim-store — not free-form model prose |
| **ST-2** | α-renaming opaque ids in the store MUST induce only corresponding renames in admissible tool calls (equivariance) — or calls pass through `EquivarianceWrap` |
| **ST-3** | No product claim of “agent satisfies business FO-CTL” without Spike STEAD exit + finite-domain story |
| **ST-4** | MCP/CLI schemas listed in `07-system-design/icd/` must cite ST-1…3 |
| **ST-5** | Harness rejects tool calls whose ids are not present in the current snapshot (no hallucinated handles) |

## Explicitly deferred

- Canonical deployment wrapper proving equivariance for arbitrary base agents  
- PSPACE FO-CTL checker over our registry  

Spike: `12-delivery/spike-charters/SPIKE-STEAD-equivariance.md`.

## Why this is not optional fluff

If we ship MCP `fitness_check` / `resolve` that accept LLM-invented bean names,
we recreate STEAD’s failure mode on day one — even with a perfect graph+lock core.

---
title: Stateful Tool-Enabled Agentic Deployment tool-boundary constraints — specification
status: DRAFT
date: '2026-08-10'
arxiv: '2608.03609'
paper_title: 'Formal Verification of Agentic Systems over Operational Data'
---

# Stateful Tool-Enabled Agentic Deployment constraints (product specification)

We **do not** implement First-Order Computation Tree Logic model checking in
the minimum viable product. We **do** adopt the paper’s warning (*Formal
Verification of Agentic Systems over Operational Data*): a large language
model + tools over relational/operational data is easy to get *formally*
wrong. Design the tool surface so we don’t paint into that corner.

A **Stateful Tool-Enabled Agentic Deployment** is the paper’s name for an
agent + tool harness over persistent operational data.

Whole words in prose — see root `GLOSSARY.md`.

## Adopted constraints (Wave 0 / Wave 1)

| ID | Constraint |
| --- | --- |
| **ST-1** | Tool parameters that name entities (bean, symbol, edge, path, claim) MUST be typed identifiers from Registry / Source Code Index Protocol / claim-store — not free-form model prose |
| **ST-2** | α-renaming opaque identifiers in the store MUST induce only corresponding renames in admissible tool calls (equivariance) — or calls pass through `EquivarianceWrap` |
| **ST-3** | No product claim of “agent satisfies business First-Order Computation Tree Logic” without Spike exit + finite-domain story |
| **ST-4** | Model Context Protocol / command-line interface schemas listed in `07-system-design/icd/` must cite ST-1…3 |
| **ST-5** | Harness rejects tool calls whose identifiers are not present in the current snapshot (no hallucinated handles) |

## Explicitly deferred

- Canonical deployment wrapper proving equivariance for arbitrary base agents  
- PSPACE First-Order Computation Tree Logic checker over our registry  

Spike: `12-delivery/spike-charters/SPIKE-STEAD-equivariance.md`.

## Why this is not optional fluff

If we ship Model Context Protocol `fitness_check` / `resolve` that accept
large-language-model-invented bean names, we recreate this paper’s failure
mode on day one — even with a perfect graph + lock core.

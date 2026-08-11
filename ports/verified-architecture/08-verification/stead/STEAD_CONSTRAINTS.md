---
title: Stateful Tool-Enabled Agentic Deployment tool-boundary constraints — specification
status: DRAFT
date: '2026-08-10'
arxiv: '2608.03609'
paper_title: 'Formal Verification of Agentic Systems over Operational Data'
---

# STEAD constraints (product specification)

MVP **does not** ship FO-CTL model checking. **Embody** 2608.03609 warning:
LLM+tools over operational data is easy to get formally wrong. Public
equivariance-wrapper engines found: **0** — ST-2 remains Spike.

Whole words — root `GLOSSARY.md`.

## Embody (Wave 0/1 design)

| ID | Constraint | Fail-mode |
| --- | --- | --- |
| **ST-1** | Entity params typed from Registry/SCIP/claim-store — not free-form model prose | Free-text bean → reject |
| **ST-2** | α-rename in store ⇒ corresponding rename in admissible calls (or `EquivarianceWrap`) | Non-equivariant call → reject |
| **ST-3** | No “agent satisfies business FO-CTL” without Spike exit + finite-domain story | Claim without exit → refuse |
| **ST-4** | MCP/CLI schemas in `07-system-design/icd/` cite ST-1…3 | Schema without cite → incomplete |
| **ST-5** | Harness rejects ids absent from current snapshot | Invented handle success → reject |

## Deferred

Canonical deployment wrapper for arbitrary agents; PSPACE FO-CTL checker.

Spike: `12-delivery/spike-charters/SPIKE-STEAD-equivariance.md`.

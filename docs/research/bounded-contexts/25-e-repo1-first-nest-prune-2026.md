---
title: E-REPO1 — first BC nest + future-facing prune (semantic_eval, docs_site)
status: APPROVED Implement Spec (user-directed tip 2026-08-10)
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
parent:
  - docs/research/bounded-contexts/21-ddd-repository-structure-options-2026.md
  - docs/research/bounded-contexts/24-ddd-repo-structure-landing-gaps-2026.md
  - DOMAIN_MAP.md
related:
  - docs/research/bounded-contexts/20-tach-dependency-blueprint-2026.md
  - docs/design/tools_bc_inventory.json
do_not:
  - dissolve scanning/compliance tools before pipeline↔scanning cycle-break
  - delete root skills/ without equality-gate rewrite (Cursor resolve path)
  - big-bang tools/ git-mv
  - weaken fail_under 98.7 / complexipy ≤5 / LOC ≤225
spec_gate: APPROVED E-REPO1-A (2026-08-10) — REPO1-A1–A6
---

# E-REPO1-A — aggressive first nest + prune

**User ask:** implement a future-facing prune and structural refactor from the
E-REPO research packet; open a PR and learn from CI.

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

## External evidence (required for design-shaped tip)

| Claim | Tier | Cite |
| --- | --- | --- |
| Bounded-context packaging beats shallow technical folders for change isolation | Evidenced | Evans / Vernon practice; survey framing in arXiv [2303.08998](https://arxiv.org/abs/2303.08998) (modular monolith coupling) |
| Explicit module boundaries + cycle refusal as fitness function | Evidenced | [tach](https://github.com/gauge-sh/tach) docs; this repo `tach.toml` `[Confirmed]` |
| Stable façade / shim across moves (invoke SoT) | Confirmed | DOMAIN_MAP G-INVOKE; gap_probe tools shim pattern |

DeepWiki used only as orientation (not sole external cite).

## One-page verdict

| Move | Stance |
| --- | --- |
| Nest `semantic_eval_*` → `doc_engine.semantic_eval` + tools `-m` shims | **Embody** (DOMAIN_MAP first nest; no G-CYCLE edge) |
| Nest `build_docs_site` → `doc_engine.docs_site` + shim; prune dead `_find_mkdocs_yml` | **Adopt** |
| Leave `doc_tag_utils` in tools (shared vocab) | **Defer** re-home |
| Delete root `skills/` mirror | **Refuse this tip** — equality gate + Cursor resolve; Spec retire later |
| Scanning / gates dissolve | **Refuse this tip** — cycle-break first |

## Approve REPO1-A1–A6

| ID | Decision |
| --- | --- |
| **A1** | Create `src/doc_engine/semantic_eval/` with `confirmed`, `mermaid`, `scan`; public package `__init__` |
| **A2** | `tools/semantic_eval_*.py` become thin re-export / `-m` shims (helpers keeps façade poke surface) |
| **A3** | Create `src/doc_engine/docs_site/`; `tools/build_docs_site.py` shim; delete unused `_find_mkdocs_yml` |
| **A4** | Inventory `move_status=nested` for moved modules; DOMAIN_MAP task order update |
| **A5** | Root `skills/` stays byte-equal mirror this tip; README marks future retire |
| **A6** | Verify: claims, inventory gate, semantic_eval pytest, adapter layout, ruff on touched |

Human / user-directed Approve of A1–A6 = this tip may Implement.

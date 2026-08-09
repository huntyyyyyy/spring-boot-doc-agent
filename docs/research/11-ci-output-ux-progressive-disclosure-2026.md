---
title: CI / script output UX — summary-first progressive disclosure (2026)
status: SPEC APPROVED E-UX0 — implement E-UX1 vertical slice
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine CI façades + quality-gates
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - src/doc_engine/ci/github_step_summary.py
do_not:
  - weaken fail_under 98.7, complexipy ≤5, LOC ≤225
  - introduce rich/emoji dashboards as CI SoT
  - treat LLM log-summarizers as merge proof
  - boil every scripts/ci façade in one tip
spec_gate: APPROVED E-UX0 (2026-08-09) — human green-light; land E-UX1 on tip
---

# Principal memo: CI output UX (summary-first)

**Question:** Can we modernize script/CI output so humans (and agents) get a
digestible headline first, with deeper logs available on demand — without a new
logging product or SoT theater?

## 0. One-page verdict

| Stance | Choice |
| --- | --- |
| **Embody** | One report object → dual sinks: headline (stdout + step summary) + detail (`::group::` / `<details>`) |
| **Adopt** | GitHub Actions log groups + `$GITHUB_STEP_SUMMARY` markdown; reuse `github_step_summary` + GapAverage dual presenters `[Evidenced]` |
| **Refuse** | `rich` as CI dependency; emoji dashboards; LLM summarizers as gates; rewriting all façades at once |

**Highest-leverage slice (E-UX1):** `doc-engine quality-gates` rollup + grouped
gate noise + align coverage/gap writers onto shared append.

## 1. Evidence

| Claim | Tier | Source |
| --- | --- | --- |
| Job summaries + collapsible groups are the GHA progressive-disclosure tools | Evidenced | GitHub Actions job summary / `::group::` docs; PowerShell CI log-group PR |
| Verbose content belongs behind explicit disclosure | Evidenced | github/gh-aw step-summary hierarchy PR |
| This repo already has dual text/markdown for gap-average + thin summary façades | Confirmed | `GapAverageReport`, adequacy/timing presenters, `github_step_summary` |
| quality-gates streams tool noise then a thin text summary; little step-summary | Confirmed | `quality_gates.py` / `quality_gate_checks._run` |
| coverage_run_summary overwrites step summary; gap-average bypasses validated append | Confirmed | `scripts/ci/coverage_run_summary.py`, `coverage_gap_average._append_github_summary` |

## 2. Decisions (E-UX0)

| ID | Decision |
| --- | --- |
| U1 | Summary-first: PASS/FAIL table before/above raw tool dumps in human sinks |
| U2 | Detail-on-demand: wrap each gate subprocess in `::group::{label}` when `GITHUB_ACTIONS=true` |
| U3 | One append contract: all step-summary writers use `doc_engine.ci.github_step_summary` |
| U4 | quality-gates emits markdown rollup to `$GITHUB_STEP_SUMMARY` when set (no-op locally) |
| U5 | Sensor vs SoT wording stays explicit (gap-average remains advisory) |
| U6 | Defer: claims/code_quality headline+details; `pre_pr`→Actions mirroring; JSON receipts beyond existing `pre_pr` |
| U7 | No `rich` / no emoji-heavy summaries |

## 3. Epic

### E-UX0 — Spec (this memo) — **DONE Approve**

### E-UX1 — quality-gates + append alignment

| Ticket | Acceptance |
| --- | --- |
| UX1-1 | `_run` emits `::group::` / `::endgroup::` under Actions |
| UX1-2 | Markdown rollup from same results as text summary; append via `github_step_summary` |
| UX1-3 | `coverage_run_summary` appends (no overwrite); gap-average uses shared append |
| UX1-4 | Tests for presenters + append; complexipy ≤5; LOC ≤225; claims OK |

### E-UX2 — later

`check_code_quality` / `check_repo_claims` headline + `<details>` issue lists.

## 4. Invariants

fail_under 98.7 · complexipy ≤5 · LOC ≤225 · no utils bag · policy C-A (no heredocs) · SDD one tip.

---
category: CI / suite stalking sensors / oracle telemetry
status: APPROVED — SPEC GATE E-RUN0 (2026-08-09)
date: '2026-08-09'
approved_policies: R1-R8
implement_now: D1 D2 D17
claim_tiers: Evidenced / Confirmed / Unknown
research: docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
title: 'Design memo: suite-stalking sensors (E-RUN v1)'
related: []
last_reviewed: '2026-08-10'
---

# Design memo: suite-stalking sensors (E-RUN v1)

> **APPROVED — SPEC GATE E-RUN0 (2026-08-09)**
>
> Principal / implementer chat recorded **Approve** of policies **R1–R8**.
> Implement epic **E-RUN1** is unblocked for **D1 + D2 + D17** only. Does not
> reopen fail_under **98.7**, policy **16-A**, E-TEST2 (suite-wide `-n`), or
> in-tree Rust.

**Spec record**

| Field | Value |
| --- | --- |
| Policies | **R1–R8** Approved |
| Implement now | **D1** durations inventory · **D2** plateau attribution · **D17** pre-pytest cascade clarity |
| Defer / refuse this stream | **D3** rpytest · **D5/D6** oracle shard/`-n` · **D8** LLM flake triage · **D9** NameRTS · **D12** OTel · **D20** in-tree Rust |
| Research | [`docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md`](../research/08-rust-test-runners-bottlenecks.md) |
| Backlog | [`docs/research/quality-backlog.md`](../research/quality-backlog.md) P7 |

---

## 1. Problem

Oracle CI mid-suite plateaus and `coverage.xml missing` summaries leave agents
without a **rebuildable bottleneck / cascade inventory**. Industry “Rust
stalker” products bundle runner swap, RTS, and flake LLM triage — most of that
is SoT-hostile here. `[Confirmed]` research **08**

---

## 2. Locked product shape (v1)

| Concern | Choice |
| --- | --- |
| Machine SoT for durations | pytest `--junitxml` on the **3.11** cov cell only |
| Presentation | GitHub step summary via `doc_engine.ci.suite_timing` + thin `scripts/ci` façade |
| Cascade (D17) | When `coverage.xml` absent, state that pre-pytest gates may have failed — sensor only |
| Plateau (D2) | Path-prefix buckets: `gate_tools`, `repo_claims_real`, `run_manifest`, `other` |
| Oracle argv | Keep `--cov-fail-under=${COV_FAIL_UNDER}` / **98.7**; single-writer `coverage.xml` |

Sensors never claim the Cover% floor.

---

## 3. Package sketch (SOLID / DDD)

Concept package `doc_engine.ci.suite_timing` (not `utils/`):

| Module | SRP |
| --- | --- |
| `duration_records` | Immutable duration / report value objects |
| `junit_duration_parse` | Parse junitxml → records |
| `plateau_buckets` | Node id → plateau label |
| `pre_pytest_cascade` | D17 markdown when coverage xml missing |
| `github_timing_summary` | Step-summary presenter (OCP: new sinks = new modules) |

LOC ≤225 / complexipy ≤5 per file; TDD under `tests/ci/test_suite_timing*.py`.

---

## 4. Non-goals

- Replacing pytest with rpytest on the cov cell
- Suite-wide xdist / `coverage combine`
- NameRTS / pre_pr selection (E-RUN4)
- In-tree Rust / Cargo workspace

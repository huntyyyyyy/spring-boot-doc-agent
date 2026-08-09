---
category: Coverage climb / measure feedback-loop architecture
status: APPROVED — SPEC GATE E-CM0 (2026-08-08)
research date: 2026-08-08
approved_decisions: 1-31
artifact_policy: 16-A
claim tiers: Evidenced / Confirmed / Unknown
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
---

# Design memo: climb/measure feedback-loop architecture

> **APPROVED — SPEC GATE E-CM0 (2026-08-08)**
>
> Principal / implementer chat recorded **Approve** of synthesis decisions
> **1–31** with climb artifact policy **16-A**. Dual-mode implementation is
> unblocked under Epic **E-CM1** (single stream). Do not reopen fuzzy/PID green,
> scoped `fail_under` as repo floor, or climb writing `coverage.xml`.

**Spec record**

| Field | Value |
| --- | --- |
| Decisions | **1–31** Approved (synthesis §5) |
| Policy **16** | **16-A** — climb → `coverage.climb.xml`; oracle SoR → `coverage.xml` only |
| Banner **11** | Required on climb; **not** sufficient alone (filename is the contract) |
| Branch / PR | `wave1-gates-untrusted-tree-hygiene` / [#94](https://github.com/huntyyyyyy/spring-boot-doc-agent/pull/94) |
| Synthesis SoT | [`docs/research/se-quality-synthesis-2026-08-08.md`](../research/se-quality-synthesis-2026-08-08.md) |
| Backlog | [`docs/research/quality-backlog.md`](../research/quality-backlog.md) |

**Status at research tip:** Synthesis + constitution rule/skill at `c9ffdbb`.
MeasureRun/PathCohesion live on this wave1 tip — land E-CM1 here (decision **12**).

**Claim tiers:** `[Evidenced]` = primary docs/code/issues cited · `[Confirmed]` = local seams + docs agree · `[Unknown]` = needs measurement (none open for **16** — locked **16-A**).

---

## 1. Problem (architecture, not typing speed)

Climb progress is gated by a **single expensive oracle** reused as the **inner-loop sensor**.

| Defect | Evidence |
| --- | --- |
| Full-suite `pytest tests/ --cov=doc_engine --cov=stf --cov-branch` is the only `MeasureRun` path | `[Evidenced]` `coverage_measure.py` hardcodes that argv; no `--scope` |
| `fail_under=98.7` applied at end of that huge run | `[Confirmed]` `pyproject.toml` + `MeasureRun.run_pytest_cov` + CI 3.11 cell |
| Gap inventory requires a cohesive full XML | `[Confirmed]` `coverage-gap-average` + CONTRIBUTING “below-floor gap-average” |
| Cross-worktree combine already burned time | `[Confirmed]` PathCohesionGuard + CONTRIBUTING single-writer contract |
| Agents block on wall-clock full remesure per batch | `[Confirmed]` process shape implied by climb suites + measure facade |

**Root cause:** one unlabeled artifact (`coverage.xml` after full pytest+cov) is treated as both **release/CI SoT** and **batch targeting sensor**. That collapses two consistency domains (DDIA: authoritative vs derived) into one wall-clock path.

---

## 2. Research (primary sources)

### 2.1 Separate CI oracle vs climb inner loop

- **CoverUp** ([arXiv:2403.16218](https://ar5iv.labs.arxiv.org/html/2403.16218)): measure → segment by *missing* lines/branches → iterate on segments → final whole-suite check. Iterative refinement ≈ half of successes. `[Evidenced]`
- **ChaCo** ([arXiv:2601.10942](https://ar5iv.labs.arxiv.org/html/2601.10942)): PR/patch-scoped cover signal for last-mile augmentation — orthogonal to whole-repo floor climb. `[Evidenced]`
- **TestForge / agentic testing**: execution + coverage as *environment feedback*, not a once-per-session full oracle. `[Evidenced]` abstracts
- **pytest-cov**: `--cov=PATH` overrides `[run] source`; `--cov-fail-under` fails on **reported total for measured sources**, not “repo truth if you narrowed source.” `[Evidenced]` [pytest-cov config](https://pytest-cov.readthedocs.io/en/latest/config.html); subset reporting caveats in [pytest-cov#528](https://github.com/pytest-dev/pytest-cov/issues/528)

**Implication for this repo:** a scoped `--cov=doc_engine.ci` run that still passes `--cov-fail-under=98.7` is a **different predicate** than whole-repo 98.7. Using the same flag without labeling modes creates a **hidden SoT**.

### 2.2 Parallel / worktree / path pitfalls

- coverage.py: parallel → distinct `.coverage.*`; combine needs path identity; `[paths]` / `relative_files`; debug with `--debug=pathmap`. `[Evidenced]` [cmd_combine](https://coverage.readthedocs.io/en/latest/commands/cmd_combine.html)
- Windows / relative_files / combine hazards: [#903](https://github.com/nedbat/coveragepy/issues/903), [#991](https://github.com/nedbat/coveragepy/issues/991), [#1752](https://github.com/coveragepy/issues/1752), [#2072](https://github.com/coveragepy/issues/2072). `[Evidenced]`
- This tree already encodes the lesson: **never combine across worktrees**; wipe local `.coverage*`; PathCohesionGuard rejects foreign `wt-*` paths. `[Confirmed]` CONTRIBUTING + `PathCohesionGuard`

### 2.3 Fail-fast / incremental without stale SoT

Industry split that matches CoverUp’s two phases:

| Signal | Role | Staleness |
| --- | --- | --- |
| Whole-repo fail_under | Authoritative floor | Fresh full measure only |
| Below-floor list / package Cover% | Derived climb inventory / accelerator | Explicitly derived; refresh on cadence |
| diff-cover on changed lines | New-code gate (already here) | Needs XML + git merge-base |

diff-cover is already the **new-code** hard gate (`quality-gates`). It is **not** a substitute for below-floor climb inventory (green files stay out of gap-average by design). `[Confirmed]` CONTRIBUTING table.

### 2.4 Matrix pattern (already applied)

Canonical cov cell = **Python 3.11 only** for pytest-cov / fail_under / XML upload; 3.10/3.12 plain pytest. `[Confirmed]` `ci.yml` + CONTRIBUTING. That removes 3× matrix cov cost; it does **not** fix the **local climb** full-suite loop.

### 2.5 Lever ranking for *this* monorepo

| Lever | Verdict | Why |
| --- | --- | --- |
| Explicit `oracle` vs `climb` modes + scoped `--cov` | **Primary** | Matches CoverUp; pytest-cov source override is the intended narrowing tool |
| Reuse last **cohesive** full measure for gap list | **Primary** | Inventory is derived; don’t remesure world to pick next file |
| `COVERAGE_FILE` / per-tree wipe | **Already landed** | Keep; don’t invent cross-tree combine |
| diff-cover | **Keep as PR gate; not climb SoT** | Wrong granularity for below-floor files |
| pytest-xdist on scoped runs | **Optional later** | Supported; adds combine/path surface; **not** required for first win |
| Rust / SlipCover | **Out of scope** | Refuse by default (rust-stack-fit memo) |

### 2.6 Operability (DDIA)

- Operability: predictable modes, good defaults, visibility. `[Evidenced]` secondary
- Single SoT vs derived views: full 3.11 measure = SoT; gap list / scoped Cover% = **derived**, rebuildable, never silently promoted. `[Evidenced]` secondary
- Local prose already says “do not treat a retrieved/stale artifact… as the Cover% oracle” — but the CLI still only exposes the oracle path until E-CM1. `[Confirmed]`

---

## 3. Current seams (what not to break)

Already cohesive (LOC from tip):

- `PathCohesionGuard`  
- `MeasureRun` (full-suite only until E-CM1)  
- `CoverageReport` / `GapAverageReport` split  
- CLI facades for `coverage-measure` / `coverage-gap-average`  
- CI: 98.7 floor + 3.11-only cov + diff-cover new-code  

`cli.py` stays a thin facade; coverage parsers live in `cli_gate_parsers.py` (no utils bag).

---

## 4. Alternatives considered

**A. Status quo** — full measure every batch.  
Reject: same defect.

**B. Scoped `--cov` only, still `fail_under=98.7` unlabeled**  
Reject: false oracle (pytest-cov source override).

**C. diff-cover as climb driver**  
Reject as primary: already new-code gate; misses unchanged below-floor files.

**D. Cross-worktree combine + `[paths]`**  
Reject: contradicts landed single-writer/cohesion contract; coveragepy pathmap risk.

**E. xdist-first on full suite**  
Defer: may cut wall-clock but keeps wrong *granularity*; more combine surface before mode separation.

**F. Dual modes (oracle vs climb) + derived gap inventory** ← **approved**

**G. Climb writes no XML (policy 16-B)**  
Reject for v1 — agents invent unlabeled temps (worse dual-write). **16-A** locked.

---

## 5. Approved design

```text
                    ┌─────────────────────────────┐
                    │  ORACLE (CI / release SoT)  │
                    │  mode=oracle (default)      │
                    │  full tests/ + doc_engine+stf│
                    │  fail_under=98.7            │
                    │  PathCohesionGuard          │
                    │  → coverage.xml (authoritative)│
                    └──────────────┬──────────────┘
                                   │ rebuilds
                                   ▼
                    ┌─────────────────────────────┐
                    │  DERIVED: GapAverageReport  │
                    │  below-floor list (targeting)│
                    │  never fail_under substitute │
                    │  binds coverage.xml only     │
                    └──────────────┬──────────────┘
                                   │ guides
                                   ▼
                    ┌─────────────────────────────┐
                    │  CLIMB (accelerator only)   │
                    │  mode=climb --scope PKG     │
                    │  --cov=PKG [+ test paths]   │
                    │  NO whole-repo fail_under   │
                    │  → coverage.climb.xml (16-A)│
                    │  banner: NOT CI ORACLE      │
                    └─────────────────────────────┘
```

**Semantics (approved)**

1. **`oracle`** = today’s `coverage-measure` (default). Only path that may assert whole-repo 98.7 / write `coverage.xml`.
2. **`climb`** = scoped source (+ optional pytest path args). Prints scope Cover% / missing; **refuses** to claim whole-repo floor. Writes **`coverage.climb.xml` only** (policy **16-A**). Exit mirrors pytest rc; never encodes floor.
3. **Gap targeting** = last cohesive **oracle** XML via `coverage-gap-average` (hard-bind default `coverage.xml`; refuse climb artifact as inventory SoT).
4. **xdist**: out of v1 (decision **8**).
5. **Docs**: CONTRIBUTING table — Oracle vs Climb vs Gap vs diff-cover.
6. **Impl shape**: `MeasureMode` strategies / hexagonal ports (OCP); shared wipe + PathCohesion; ≤225 LOC modules; no utils dump; descriptive names (no `m`/`o`/`c`).

---

## 6. Design decisions — APPROVED (1–31)

Skeleton **1–12**, quality bar **13–16** (with **16-A**), taxonomy/frameworks/metrics/dynamics **17–31** as listed in the synthesis memo §5. Amendments in this Spec:

- **3 / v1:** no `--climb-floor` advisory flag in E-CM1.
- **16:** **A** only — `coverage.climb.xml` vs `coverage.xml`.
- **11:** banner required; filename contract is authoritative.

---

## 7. Phase 2 / implementation

**E-CM0 exit met** — Spec approved in-repo.  
**Next:** Epic **E-CM1** single stream (size preflight → strategies → climb path → gap bind → CLI).  
Invariants: `fail_under` 98.7, complexipy ≤5, LOC ≤225, no utils, SDD one tip writer, no force-push tip thrash.

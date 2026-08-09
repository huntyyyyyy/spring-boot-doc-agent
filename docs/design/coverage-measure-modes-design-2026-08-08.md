---
category: Coverage climb / measure feedback-loop architecture
status: AWAITING DESIGN CONFIRMATION — NOT IMPLEMENTED
research date: 2026-08-08
claim tiers: Evidenced / Confirmed / Unknown
---

# Design memo: climb/measure feedback-loop architecture

> **AWAITING DESIGN CONFIRMATION — NOT IMPLEMENTED**
>
> Phase 1 research complete. No dual-mode behavior change landed from this memo.
> Approve/reject (or amend) decisions **1–12** before any implementation.

**Status at research tip:** Tip inspected: `wt-cov-measure-fix` @ `bee310d` (`wave1-cov-path-cohesion`). No incomplete scoped-measure WIP to park.

**Claim tiers:** `[Evidenced]` = primary docs/code/issues cited · `[Confirmed]` = local seams + docs agree · `[Unknown]` = needs measurement or product choice.

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
- Windows / relative_files / combine hazards: [#903](https://github.com/nedbat/coveragepy/issues/903), [#991](https://github.com/nedbat/coveragepy/issues/991), [#1752](https://github.com/coveragepy/coveragepy/issues/1752), [#2072](https://github.com/coveragepy/coveragepy/issues/2072). `[Evidenced]`
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
| diff-cover | **Keep as PR gate; not climb SoT** | Wrong granularity for 81 below-floor files |
| pytest-xdist on scoped runs | **Optional later** | Supported ([xdist docs](https://pytest-cov.readthedocs.io/en/latest/xdist.html); DeepWiki DistMaster/DistWorker); adds combine/path surface; **not** required for first win |
| Rust / SlipCover | **Out of scope** | User: no Rust |

DeepWiki ([pytest-cov controllers](https://deepwiki.com/pytest-dev/pytest-cov/2.2-coverage-controllers-and-execution-modes), [xdist](https://deepwiki.com/pytest-dev/pytest-cov/3.3-distributed-testing-with-pytest-xdist)): xdist uses suffix’d data + master combine — fine **inside one checkout**, dangerous if agents treat worker shards as oracle or mix trees. `[Evidenced]` secondary wiki + primary docs.

### 2.6 Operability (DDIA)

- Operability: predictable modes, good defaults, visibility ([DDIA ch.1 notes](https://www.mintlify.com/ps06756/Designing-Data-Intensive-Applications/chapters/chapter-01-reliable-scalable-maintainable)). `[Evidenced]` secondary
- Single SoT vs derived views ([DDIA ch.12 notes](https://www.mintlify.com/ps06756/Designing-Data-Intensive-Applications/chapters/chapter-12-future-data-systems)): full 3.11 measure = SoT; gap list / scoped Cover% = **derived**, rebuildable, never silently promoted. `[Evidenced]` secondary
- Local prose already says “do not treat a retrieved/stale artifact… as the Cover% oracle” — but the CLI still only exposes the oracle path. `[Confirmed]`

---

## 3. Current seams (what not to break)

Already cohesive (LOC from tip):

- `PathCohesionGuard` ~76 LOC  
- `MeasureRun` ~150 LOC (full-suite only)  
- `CoverageReport` / `GapAverageReport` split  
- CLI facades for `coverage-measure` / `coverage-gap-average`  
- CI: 98.7 floor + 3.11-only cov + diff-cover new-code  

`cli.py` ~368 LOC — above 225; any new UX should stay thin facades, not grow a god module.

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

**F. Dual modes (oracle vs climb) + derived gap inventory** ← **recommend**

---

## 5. Recommended design (not implemented)

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
                    └──────────────┬──────────────┘
                                   │ guides
                                   ▼
                    ┌─────────────────────────────┐
                    │  CLIMB (accelerator only)   │
                    │  mode=climb --scope PKG     │
                    │  --cov=PKG [+ test paths]   │
                    │  NO whole-repo fail_under   │
                    │  optional local floor later │
                    │  banner: NOT CI ORACLE      │
                    └─────────────────────────────┘
```

**Semantics**

1. **`oracle`** = today’s `coverage-measure` (default). Only path that may assert whole-repo 98.7.  
2. **`climb`** = scoped source (+ optional pytest path args). Prints scope Cover% / missing; **refuses** to claim whole-repo floor. Exit 0/1 = pytest/process health, not repo floor.  
3. **Gap targeting** = last cohesive oracle XML via `coverage-gap-average` (or `--skip-pytest` on oracle after intentional full run). Cadence: after N batches / before PR / when inventory empty — not every micro-batch.  
4. **xdist**: opt-in flag on climb only in a later PR; default off.  
5. **Docs**: CONTRIBUTING table — Oracle vs Climb vs Gap vs diff-cover.  
6. **Impl shape**: extend `MeasureRun` via strategy/params (OCP), or small `ClimbMeasure` sibling; CLI thin; ≤225 LOC modules; no utils dump; no stale-artifact SoT.

---

## 6. Design decisions — approve / reject

1. **Dual modes on one entry point:** `doc-engine coverage-measure --mode oracle|climb` (default `oracle`), not a second top-level command.  
2. **Climb scope:** package/module via `--scope doc_engine.ci` → pytest `--cov=<scope>`; optional trailing pytest paths for suite narrowing.  
3. **Climb must not apply whole-repo `fail_under=98.7`.** Optional later: `--climb-floor` as *local advisory* only, never CI SoT.  
4. **Gap inventory stays derived from last cohesive oracle XML**; climb does not rewrite the targeting SoT.  
5. **Oracle cadence policy (docs):** remesure oracle after climb batch / before PR / when targeting from stale XML — not every file edit.  
6. **Keep PathCohesionGuard + single-writer wipe** for both modes; still forbid cross-worktree combine.  
7. **Do not weaken CI 98.7** on 3.11; do not add cov to 3.10/3.12.  
8. **xdist:** out of v1; optional climb-only follow-up.  
9. **diff-cover:** unchanged as new-code gate; not climb inventory.  
10. **cli.py:** thin facade only; if still >225 after wire-up, split coverage parsers into existing `_add_coverage_cli_parsers` module (or sibling), not a utils bag.  
11. **Banner/stderr contract:** climb output must say `mode=climb (not CI oracle)` so agents cannot mistake it for floor proof.  
12. **Target branch for eventual impl:** land on wave1 tip that already has MeasureRun/PathCohesion (`wave1-cov-path-cohesion` / merge into `wave1-gates-untrusted-tree-hygiene`), not a side branch that forks the SoT story.

---

## 7. Phase 2

**Awaiting design confirmation.**

Please approve/reject (or amend) bullets **1–12**. On confirmation only: implement climb mode + tests + CONTRIBUTING, then timed scoped-vs-full demo — without touching the 98.7 canonical cell.

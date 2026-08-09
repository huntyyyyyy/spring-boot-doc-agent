---
title: Suite stalking feature space — runners, telemetry, selection, triage (2026)
status: RESEARCH COMPLETE — Spec gate not yet approved (E-RUN0)
date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
prefer_sources: "2026 primary (arXiv / product docs / OTel semconv); older only as contrast"
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
siblings:
  - docs/research/06-test-suite-bounded-contexts-parallel.md
  - docs/research/07-ci-workflow-modularity.md
  - docs/design/rust-stack-fit-memo-2026-08-08.md
related:
  - docs/research/pr-94-followup-oracle-stabilize.md
  - docs/research/quality-backlog.md
  - docs/research/01-coverage-oracle-climb-solid.md
do_not:
  - weaken fail_under=98.7 or replace oracle with runner green
  - suite-wide -n / xdist / rpytest shard of the cov cell without E-TEST2 Spec
  - in-tree Rust / Cargo workspace for this question
  - LLM-as-judge of flaky vs real as merge SoT
  - RTS that skips the oracle cell on merge
---

# 08 — Suite stalking feature space vs this oracle (2026)

Sibling to **06–07**, [rust-stack-fit](../design/rust-stack-fit-memo-2026-08-08.md),
and **01** (oracle vs climb). Expands beyond “install rpytest” into a **feature
map**: what a stalker-class capability can mean for *this* Python CLI product,
which dimensions earn Spec tickets, and which are category errors.

**Prefer 2026 primaries.** Pre-2026 cited only as contrast.

**Claim tiers:** `[Evidenced]` primary · `[Confirmed]` this repo · `[Unknown]`
needs measure or Spec choice.

---

## 1. Frame

**Symptom cluster:**

1. Mid-suite progress plateaus feel like runner stalls.
2. Agents and humans lack a durable **bottleneck / failure inventory** across
   oracle vs ABI.
3. Industry “Rust stalkers” (warm daemon, flake reports, slow marks) look like
   a single product — they are actually a **bundle of dimensions**.

**Category errors to refuse (unchanged core):**

1. Faster *runner* ≠ Cover% floor proof.
2. Progress-% stalls ≠ collection/startup cost here.
3. Suite-wide parallel ≠ E-TEST quarantine (**06** / **T-A**).
4. LLM flaky-vs-bug as merge SoT (synthesis **20**).
5. Selective testing that **skips the oracle** on merge.

**Real design question:** Which stalker dimensions become **sensors** under
DDIA (rebuildable views), which stay **local accelerators**, and which must
never touch the single-writer oracle?

---

## 2. Confirmed inventory (this repo)

| Fact | Value | Tier |
| --- | --- | --- |
| Oracle SoT | 3.11 `pytest tests/` + `fail_under=98.7` + `coverage.xml` | `[Confirmed]` |
| ABI | `domain_*` shards; no cov combine | `[Confirmed]` E-TEST1 |
| Plateau map (`domain_ci_meta`) | ~28% gate_tools · ~50–55% real `repo_claims` · ~57–62% run_manifest/scan | `[Confirmed]` 2026-08-09 |
| Rust in-tree | None; pinned CLIs (ruff, ast-grep) | `[Confirmed]` |
| Existing adjacent seams | `pre_pr` path-risk modes · `coverage_run_summary` · gap-average · Tach (local) · incident mutators | `[Confirmed]` |
| xdist | Not a dep; E-TEST2 deferred | `[Confirmed]` |

---

## 3. Primary sources (prefer 2026)

### 3.1 Flaky / intermittent CI

| Source | Claim | Tier |
| --- | --- | --- |
| [2607.09345](https://arxiv.org/abs/2607.09345) | Code-only detectors overfit protocols; many flakes need CI logs / same-commit evidence; reruns costly | `[Evidenced]` |
| [2602.05465](https://arxiv.org/abs/2602.05465) | LLM on test code alone weak; need extra context | `[Evidenced]` |
| [2601.22264](https://arxiv.org/abs/2601.22264) FlaXifyer | Intermittent **jobs** ≫ unit flakes; log triage + interpretability | `[Evidenced]` sensor-shaped |

### 3.2 Selection / RTS (Python-relevant)

| Source | Claim | Tier |
| --- | --- | --- |
| [2605.25356](https://arxiv.org/abs/2605.25356) NameRTS | Name-graph RTS for Python: ~70% test-file skip, ~46% time cut, high safety on commits | `[Evidenced]` · **Adopt shape for pre-PR / agent loops only** |
| [2509.10279](https://arxiv.org/abs/2509.10279) T-TS | ML test selection without coverage maps; industrial speedups | `[Evidenced]` · transfer = advisory; not oracle skip |
| ChaCo [2601.10942](https://arxiv.org/abs/2601.10942) | Patch-scoped cover augmentation ≠ whole-repo floor | `[Evidenced]` · already in **01** |

### 3.3 Behavioral / CI telemetry

| Source | Claim | Tier |
| --- | --- | --- |
| [2604.16933](https://arxiv.org/abs/2604.16933) Behavioral Co-Versioning | CI discards rich run-time signals → pass/fail; archive selected observations keyed by commit/test | `[Evidenced]` · Adopt **narrow** (durations/failures), refuse full behavior DB as SoT |
| [OTel CI/CD semconv](https://opentelemetry.io/docs/specs/semconv/cicd/cicd-metrics/) (2025–26 RC) | Pipeline/job/step metrics & resources | `[Evidenced]` · Adopt only if cheap; refuse high-cardinality run IDs as required |

### 3.4 Suite efficiency / utility (transfer carefully)

| Source | Claim | Tier |
| --- | --- | --- |
| [2601.11647](https://arxiv.org/abs/2601.11647) RL CI workflow | Dynamic scope selection | `[Evidenced]` · **Refuse** as oracle omit |
| [2603.01409](https://arxiv.org/abs/2603.01409) MIST-RL | Utility over quantity for tests/mutants | `[Evidenced]` · already matches incident-seeded mutators |

### 3.5 Rust-class pytest runner (product)

| Source | Claim | Tier |
| --- | --- | --- |
| [rpytest](https://docs.neullabs.com/rpytest/) / PyPI 2026 | Warm daemon; `-n`; shard; `--reruns` / `--flaky-report`; `--watch`; `--verify-dropin` | `[Evidenced]` |
| [BENCHMARK.md](https://github.com/neul-labs/rpytest/blob/main/BENCHMARK.md) | Synthetic wins; xdist startup can hurt tiny suites | `[Evidenced]` vendor · **Unknown** here until measured |

DeepWiki for rpytest: **Unknown** this pass.

---

## 4. Feature dimensions (scoped to this product)

Each row is a stalker-class capability. **Layer** = DDIA bind.

| # | Dimension | What it is | Layer | Stance for *this* repo | Existing seam |
| --- | --- | --- | --- | --- | --- |
| **D1** | Duration inventory | Rank slowest tests/files per cell | Sensor | **Adopt first** (`--durations` / junit timing) | none as SoT |
| **D2** | Plateau attribution | Map % stalls → named suites (claims/manifest/…) | Sensor | **Adopt** (doc + optional script over durations JSON) | CI logs only |
| **D3** | Warm re-run / daemon | Skip cold collect on TDD loops | Local accel | **Adopt optional** (rpytest spike) · never oracle-required | Tach skip (local) |
| **D4** | Watch / affected re-run | Re-run touched tests on edit | Local accel | **Adopt optional**; Tach already approximates | Tach |
| **D5** | Built-in parallel (`-n`) | Multi-worker dispatch | Parallel | **Refuse** on oracle; E-TEST2 only inside non-cov shard | ABI jobs |
| **D6** | CI sharding flags | `--shard i/n` | Parallel | **Refuse** for cov combine; ABI already path-sharded | `abi-tests.yml` |
| **D7** | Flake reruns / report | Retry fails; summarize flake | Sensor | **Adopt advisory only**; fail-closed on hard gates | — |
| **D8** | Job-failure triage | Infra vs real vs flake from **logs** | Sensor | **Adopt later** (scripted categories); LLM advisory | FlaXifyer shape |
| **D9** | RTS / NameRTS-class | Run tests reaching changed names | Accelerator | **Adopt for `pre_pr` / agent**; **Refuse** as merge oracle substitute | `pre_pr` modes |
| **D10** | Patch cover sensor | ChaCo-style last-mile | Climb sensor | **Adopt** only under climb mode (**01**/16-A) | dual-mode design |
| **D11** | Behavioral archive | Persist timings/fail signatures by commit | Sensor archive | **Adopt narrow** durations+failures artifact; refuse full I/O archive v1 | — |
| **D12** | OTel CI spans | Job/step latency metrics | Ops sensor | **Defer**; GHA logs + durations cheaper first | — |
| **D13** | Slow-timeout / kill | Mark/kill runaway tests | Gate-adjacent | **Adopt** only with Spec + known-serial quarantine | — |
| **D14** | Mutation stalker | Which mutants survive; duration per mutant | Sensor | **Embody** incident mutators; report survivors (already) | `mutate.py` |
| **D15** | Gap-average coupling | Feed slow *and* under-floor files to climb | Climb sensor | **Adopt** join view (durations ⋈ gap rows) | gap-average |
| **D16** | Path-cohesion stalker | Reject foreign/wt Cobertura paths | SoT guard | **Embody** (already PathCohesionGuard) | `coverage_path_cohesion` |
| **D17** | Gate-order / fail-fast inventory | Surface “stopped before pytest” (ruff/CQ) | Sensor | **Adopt** in summaries (missing xml cascade) | `coverage_run_summary` |
| **D18** | Agent next-action card | From D1+D8+D9: “run these nodes” | Agentic | **Adopt** as markdown receipt; never auto-merge | `pre_pr` receipt |
| **D19** | Memory/CPU of workers | Profile pytest process | Spike | **Unknown** until durations prove need | — |
| **D20** | In-tree Rust stalker | Own Cargo crate | Product | **Refuse** | rust-stack-fit |

```text
SO T (boolean)                    SENSORS (rebuildable)              LOCAL ACCEL
─────────────────────────         ─────────────────────              ───────────
fail_under 98.7                   D1 durations                       D3 warm daemon
coverage.xml (16-A)               D2 plateau map                     D4 watch / Tach
PathCohesion (D16)                D7/D8 flake·triage reports         D9 RTS pre-PR
claims / size / complexipy        D11 narrow archive                 D5/D6 only non-oracle
                                  D15 durations ⋈ gap-average
                                  D17 pre-pytest cascade
                                  D18 agent card
```

---

## 5. Wall clock (this suite) — where runners help

```text
COLD START / COLLECTION          TEST BODY
──────────────────────────       ──────────────────────────────
D3/D4 help a lot                 D1/D2/D15 measure; D9 may skip
                                 D5/D6 do not remove scan cost
```

| ~% | Region | Dimension that helps |
| --- | --- | --- |
| 28–29 | `gate_tools*` | D1; maybe D9 if unused in change |
| 50–55 | real `repo_claims` | D1/D2; body rewrite — **not** runner |
| 57–62 | manifest + scan | D1/D2; Stage-0 profile (rust-stack-fit Rank 2) if hot |
| late | mutate / metamorphic | D14; MIST-RL utility philosophy |

---

## 6. Embody / Adopt / Refuse (rolled up)

| Stance | Choice |
| --- | --- |
| **Embody** | Oracle boolean SoT; PathCohesion; incident mutators; ABI domains already |
| **Adopt (v1 Spec)** | **D1, D2, D17** — durations + plateau attribution + pre-pytest cascade clarity |
| **Adopt (v1.5)** | **D7** advisory flake report; **D15** join durations with gap-average; **D18** agent card from `pre_pr` |
| **Adopt (spike)** | **D3** rpytest `--verify-dropin` on one `domain_*`; **D9** NameRTS-shaped selection behind `pre_pr` only |
| **Defer** | **D8** log triage; **D11** archive beyond CI artifacts; **D12** OTel; **D13** timeouts; **D19** CPU profile |
| **Refuse** | **D5/D6** on oracle; **D20** in-tree Rust; LLM flake merge SoT; RTS skipping oracle; RL skip of cov cell |

---

## 7. Policies for Spec gate **E-RUN0** (proposed)

| ID | Policy |
| --- | --- |
| **R1** | Bottleneck SoT = oracle-cell durations (log or artifact), not vendor benches |
| **R2** | External runners (rpytest) only after `--verify-dropin` on a named marker set; never required for merge |
| **R3** | Oracle remains single-process cov write until E-TEST2 amends (no combine) |
| **R4** | Flake reruns / triage = advisory; hard gates fail-closed |
| **R5** | No Cargo in-repo for E-RUN |
| **R6** | RTS / Tach / warm daemon may accelerate **pre-PR and ABI**; they must not claim 98.7 |
| **R7** | Behavioral archive v1 = durations + failure node ids + gate exit cascade only |
| **R8** | Agent “next action” cards are receipts (like `pre_pr`), not SoT |

---

## 8. Epic sketch (expanded)

| Field | Content |
| --- | --- |
| **Epic** | **E-RUN** — Suite stalking without SoT dilution |
| **Goal** | Instrument bottlenecks/failures as sensors; optional local accel; oracle stays 98.7 |
| **E-RUN0** | Spec approve **R1–R8** |
| **E-RUN1** | **D1+D17:** durations on 3.11 (+ optional ABI); missing-xml cascade already explains pre-pytest fails |
| **E-RUN2** | **D2+D15:** plateau map doc/script; optional durations ⋈ gap-average worst files |
| **E-RUN3** | **D3** spike: rpytest verify-dropin + wall clock on one domain (exit: ≥15% or refuse) |
| **E-RUN4** | **D9+D18:** NameRTS-shaped / import-graph selection behind `pre_pr` + agent card (never oracle) |
| **E-RUN5** (defer) | **D7/D8** advisory flake/job triage from logs |
| **Exit** | Spec recorded; D1 in CI; spikes accept/reject; oracle command unchanged unless R3 amended |
| **Invariants** | 98.7 · 16-A · ≤5 complexipy · ≤225 LOC · T-A · no LLM-judge floor |

---

## 9. One-page verdict

| Question | Answer |
| --- | --- |
| Is “the Rust stalker” one feature? | **No** — ~20 dimensions; runner is a subset (**D3–D7**). |
| What should this project Spec first? | **D1/D2/D17** sensors — cheap, hermetic, SoT-safe. |
| Where does NameRTS / selection fit? | **pre_pr / agents (D9/D18)** — not merge oracle. `[Evidenced]` 2605.25356 |
| Behavioral co-versioning? | Narrow archive of timings/failures (**D11/R7**); refuse full runtime DB v1. `[Evidenced]` 2604.16933 |
| Will rpytest fix 50–62% stalls? | **No** — those are test bodies. `[Confirmed]` |
| Implement now? | **No** — **E-RUN0** Spec first. |

---

## 10. Adversarial checklist

- [ ] Collapsed all dimensions into “add rpytest”?
- [ ] Used RTS to skip oracle on merge?
- [ ] Treated flake reruns as green?
- [ ] Sharded cov + `coverage combine`?
- [ ] Built OTel/behavior archive before durations?
- [ ] Let LLM triage become fail_under?
- [ ] Ignored existing `pre_pr` / gap-average / PathCohesion seams?

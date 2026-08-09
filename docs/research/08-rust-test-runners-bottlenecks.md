---
title: Rust-class test runners, suite stalking, and oracle bottlenecks
status: RESEARCH COMPLETE — Spec gate not yet approved (E-RUN0)
date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
prefer_sources: "2026 primary (arXiv / product docs); older only as contrast"
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
siblings:
  - docs/research/06-test-suite-bounded-contexts-parallel.md
  - docs/research/07-ci-workflow-modularity.md
  - docs/design/rust-stack-fit-memo-2026-08-08.md
related:
  - docs/research/pr-94-followup-oracle-stabilize.md
  - docs/research/quality-backlog.md
do_not:
  - weaken fail_under=98.7 or replace oracle with runner green
  - suite-wide -n / xdist / rpytest shard of the cov cell without E-TEST2 Spec
  - in-tree Rust / Cargo workspace for this question
  - LLM-as-judge of flaky vs real as merge SoT
---

# 08 — Rust test runners & “suite stalking” vs this oracle (2026)

Sibling to **06–07** and the [rust-stack-fit memo](../design/rust-stack-fit-memo-2026-08-08.md).
Those embodied test BCs, CI YAML modularity, and **no in-tree Rust by default**.
This segment asks: when progress bars stall mid-suite and a Rust “stalker”
(daemon runner / flake reporter / slow-test tracker) looks attractive, what to
**Embody / Adopt / Refuse** for *spring-boot-doc-agent* — without confusing
**ABI green** with the **3.11 fail_under=98.7** oracle.

**Prefer 2026 primaries.** Pre-2026 work is cited only as contrast.

---

## 1. Frame

**Symptom:** ABI / domain shards show plateaus (~28–29%, ~55%, ~57%, ~62%) that
feel like “the runner is stuck.” Separately, engineers notice Rust-powered
pytest replacements (warm daemon, flaky reports, slow-test status) and ask
whether that class of tool should enter the tip.

**Category errors to refuse:**

1. Treating a faster *runner* as proof the **coverage floor** is met.
2. Treating progress-% stalls as collection/startup cost when they are
   **subprocess-heavy Python tests**.
3. Adopting suite-wide parallel dispatch as a substitute for E-TEST domain
   quarantine (**06** / policy **T-A**).
4. Using LLM flaky-vs-bug classifiers as merge SoT (synthesis **20**).

**Real design questions:**

1. Where does wall clock actually go in *this* suite?
2. What does a Rust-class runner buy vs steal (daemon, `-n`, sharding)?
3. What 2026 evidence says about flaky detection and CI optimization — and what
   transfers to a Python CLI with a single-writer Cover% SoT?

---

## 2. Confirmed inventory (this repo)

| Fact | Value | Tier |
| --- | --- | --- |
| Oracle SoT | One 3.11 `pytest tests/` cell; `fail_under=98.7`; `coverage.xml` | `[Confirmed]` E-CM0 / 16-A |
| ABI path | Marker shards (`domain_*`); **no** cov combine | `[Confirmed]` E-TEST1 |
| Progress stalls (ABI `domain_ci_meta` log) | ~28% `gate_tools` · ~50–55% real-repo `repo_claims` · ~57–62% `run_manifest` + signal/CLI | `[Confirmed]` 2026-08-09 CI paste |
| In-tree Rust | None (`Cargo.toml` absent); Rust consumed as **pinned CLIs** (ruff, ast-grep) | `[Confirmed]` rust-stack-fit memo |
| pytest-xdist | Not a dep; suite-wide `-n` refused until E-TEST2 | `[Confirmed]` **06** / backlog P5.2 |
| Mutation / flake tooling | Incident-seeded `gate_mutators`; not PIT zoo | `[Confirmed]` CONTRIBUTING |

**Reading:** the “stalker” product class (slow/flaky telemetry + warm re-runs)
overlaps **local agent loops** and **ABI diagnosis**. It does **not** remove
Stage-0 / claims / kitchen-sink subprocess cost inside the oracle cell.

---

## 3. Primary sources (prefer 2026)

### 3.1 Flaky / intermittent CI (2026)

| Source | Claim | Tier |
| --- | --- | --- |
| arXiv [2607.09345](https://arxiv.org/abs/2607.09345) — *How Far Are We from Detecting Flaky Tests?* | Code-only / CV protocols overstate detectors; many E2E flakes need **CI log + same-commit** evidence; reruns remain expensive at scale | `[Evidenced]` |
| arXiv [2602.05465](https://arxiv.org/abs/2602.05465) — *Can We Classify Flaky Tests Using Only Test Code?* | LLMs on test code alone struggle; non-determinism even at T=0; humans need extra context for sophisticated flakes | `[Evidenced]` |
| arXiv [2601.22264](https://arxiv.org/abs/2601.22264) — *FlaXifyer* | Intermittent **job** failures ≫ flaky unit tests alone; few-shot LM triage on **logs**; interpretability reduces review | `[Evidenced]` (industrial CI; transfer = advisory triage, not floor SoT) |

**Product bind:** Flake *telemetry* (reruns, slow marks, log triage) can be a
**sensor**. It must not redefine pass/fail of the 98.7 oracle or silently
quarantine fault-triggering failures as “flake.” Aligns with 2607.09345’s
warning that shortcuts hide real defects. `[Evidenced]` + `[Confirmed]` SoT.

### 3.2 CI / suite efficiency (2026) — transfer carefully

| Source | Claim | Tier |
| --- | --- | --- |
| arXiv [2601.11647](https://arxiv.org/abs/2601.11647) — RL CI/CD workflow optimization | Dynamic test-scope selection can cut overhead in simulation | `[Evidenced]` domain · **Refuse transfer** as oracle skip heuristic without Spec |
| arXiv [2603.01409](https://arxiv.org/abs/2603.01409) — MIST-RL | Scale test *utility* not quantity (mutation score ↑, suite length ↓) | `[Evidenced]` · Adopt as **philosophy** for incident-seeded mutators already here; not a runner swap |
| AgenticCI / mobile selection (2026 Zenodo) | Risk-based selection cuts wall clock on app CI | `[Evidenced]` secondary · **Refuse** as Cover% substitute |

### 3.3 Rust-class pytest runner (product docs, 2026)

| Source | Claim | Tier |
| --- | --- | --- |
| [rpytest docs](https://docs.neullabs.com/rpytest/) / [GitHub](https://github.com/neul-labs/rpytest) / PyPI 0.1.x (2026) | Rust CLI + warm Python daemon; collection/startup wins; built-in `-n`, `--shard`, `--reruns` / `--flaky-report`, `--watch`; `--verify-dropin` | `[Evidenced]` |
| [BENCHMARK.md](https://github.com/neul-labs/rpytest/blob/main/BENCHMARK.md) | Synthetic ~500-test suite: warm runs beat cold pytest; xdist worker startup can *hurt* tiny suites | `[Evidenced]` (vendor bench · **Unknown** on *this* suite until measured) |

**Category:** *external* runner binary — same adoption pattern as ruff/ast-grep
(consume Rust product), **not** in-tree PyO3. Still a **CI SoT** decision if
Actions replaces `pytest` on the cov cell.

### 3.4 Contrast (non-2026 / adjacent — not preferred SoT)

| Source | Use here |
| --- | --- |
| cargo-nextest slow-timeout / retries docs | Pattern cousin (“SLOW” status, retries); Rust-*cargo* domain, not pytest | Vocabulary only |
| Pre-2026 Chromium flaky-vs-fault work | Superseded in preference by **2607.09345** / **2602.05465** | Do not cite as tip SoT |

DeepWiki cartography for rpytest: **Unknown** (no stable DeepWiki page found
in this pass).

---

## 4. Where wall clock goes (this product)

```text
COLD START / COLLECTION          TEST BODY (this suite)
──────────────────────────       ──────────────────────────────
interpreter + plugin import      repo_claims real-tree scans
pytest collection                run_manifest + spring_signal_scan
                                 kitchen-sink / ETL chains
rpytest / warm daemon helps ↑    Rust runner barely moves ↑
```

**Plateau map `[Confirmed]`** from the pasted `domain_ci_meta` run:

| ~% | Suite region | Cost shape |
| --- | --- | --- |
| 28–29 | `gate_tools*` | path / jscpd / subprocess edges |
| 50–55 | `repo_claims_real_repo*` | whole-checkout claim checker |
| 57–62 | `run_manifest_*` CLI + signatures | multi-step CLI / scan |
| late | metamorphic / mutate sandboxes | copy + suite per mutant |

A daemon that skips re-collection helps **agent TDD loops** and **ABI retries**.
It does not make `check_repo_claims` or Stage-0 scans free.

---

## 5. Embody / Adopt / Refuse

| Stance | Choice |
| --- | --- |
| **Embody** | Boolean oracle SoT stays `pytest` (or verified drop-in) + `fail_under=98.7` + cohesive `coverage.xml`; sensors ≠ SoT (**01** / **16-A**) |
| **Embody** | Profile before native/runner adoption (rust-stack-fit; synthesis **22**) |
| **Adopt (sensor)** | `pytest --durations=N` (or equivalent) on 3.11 oracle + ABI as the **first** bottleneck SoT — hermetic, no new runtime |
| **Adopt (optional local)** | Spike **rpytest** *outside* the cov cell: `--verify-dropin` on a domain marker; measure wall clock on `domain_ci_meta` / serial domains only |
| **Adopt (telemetry)** | Duration / flake **reports** as advisory CI artifacts (never auto-green) |
| **Refuse** | Replacing 3.11 oracle `pytest` with `rpytest -n` / shard **before** E-TEST2 Spec + path-cohesion review |
| **Refuse** | In-tree Rust for test stalking |
| **Refuse** | LLM flake classifiers as merge gate (**2602.05465** + synthesis **20**) |
| **Refuse** | RL / agentic test-skip policies that omit the oracle cell (**2601.11647** transfer refuse) |
| **Refuse** | Treating ABI domain pass as “CI passed” when 98.7 is red |

---

## 6. Decision sketch (for later Spec gate **E-RUN0**)

Proposed policies (not approved until Spec):

| ID | Policy |
| --- | --- |
| **R1** | Bottleneck SoT = committed durations artifact or job log section from **oracle** cell, not vendor synthetic benches |
| **R2** | External Rust runners allowed as **dev/ABI accelerators** only after `--verify-dropin` parity on collection + exit codes for that marker set |
| **R3** | Oracle cell command remains single-process coverage write until E-TEST2 explicitly allows in-shard parallel **without** `coverage combine` |
| **R4** | Flaky reruns: advisory / non-blocking jobs only; hard gates stay fail-closed on first deterministic failure |
| **R5** | No Cargo in-repo for this epic |

---

## 7. Epic sketch (fresh-chat)

| Field | Content |
| --- | --- |
| **Epic** | **E-RUN** — Suite stalking / runner policy without SoT dilution |
| **Goal** | Evidence-bound decision: durations first; optional rpytest local/ABI; oracle stays 98.7 |
| **E-RUN0** | Spec approve **R1–R5** (this memo) |
| **E-RUN1** | Implement durations reporting on 3.11 python-gates (+ optional ABI) |
| **E-RUN2** | Optional spike: rpytest `--verify-dropin` + wall-clock vs pytest on one `domain_*` (no cov) |
| **Exit** | Spec recorded; durations in CI; spike accept/reject memo; **no** oracle command change unless R3 amended |
| **Invariants** | 98.7 · 16-A · complexipy ≤5 · LOC ≤225 · T-A · no LLM-judge floor |

**Spike exit (E-RUN2):** If rpytest does not cut ≥15% wall clock on the chosen
ABI domain **or** fails drop-in verify → **Refuse** adoption; keep durations only.

---

## 8. One-page verdict

| Question | Answer |
| --- | --- |
| Is the Rust “stalker” real? | Yes — **rpytest** (2026) fits the description: warm daemon, flake/slow-adjacent UX, parallel/shard flags. `[Evidenced]` |
| Will it fix mid-suite % stalls here? | **Mostly no** — stalls are test bodies (claims / manifest / scan). `[Confirmed]` |
| Prefer 2026 research takeaway? | Flake detection needs **execution/logs**, not code-only or LLM-on-test-source; keep sensors off the Cover% SoT. `[Evidenced]` 2607 / 2602 / 2601 |
| Implement runner swap now? | **No** — Spec **E-RUN0** first; durations (**E-RUN1**) before any runner spike |
| In-tree Rust? | **Refuse** (unchanged vs rust-stack-fit / **22**) |

---

## 9. Adversarial checklist

- [ ] Did we almost replace oracle `pytest` because ABI felt slow?
- [ ] Did vendor BENCHMARK.md substitute for *this* suite’s `--durations`?
- [ ] Did `--reruns` / flake reports risk greenwashing fault-triggering fails?
- [ ] Did `-n` / `--shard` threaten single-writer `coverage.xml`?
- [ ] Did LLM flake triage creep toward merge SoT?

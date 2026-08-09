---
title: E-CQL0 — CodeQL signals CI skip / fingerprint (when logic unchanged)
status: E-CQL0 APPROVED (2026-08-09) — merge Approve of CQ1–CQ9
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine — CI BC codeql-signals (fixture pack gate)
related:
  - docs/research/07-ci-workflow-modularity.md
  - docs/design/ci-workflow-modularity-design-2026-08-09.md
  - docs/research/08-rust-test-runners-bottlenecks.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - weaken fail_under 98.7; skip oracle cov cell; fuzzy/PID green
  - on.pull_request.paths on required CI (Pending forever)
  - treat actions/cache or restored DB as merge SoR / skip assertions
  - CodeQL overlay / diff-informed as substitute for traced fixture gate
  - ML CI-skip / RTS as gate; fatten ci.yml; utils/ grab-bag
  - conflate Stage-0 pack (codeql/spring-signals) with CI pack (spring-signals/codeql)
spec_gate: APPROVED E-CQL0 (2026-08-09) — CQ1–CQ9
---

# Principal memo: skip CodeQL signals runtime when logic unchanged

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is “always re-run CodeQL signals” wrong? | **Yes for CI wall-clock** — not wrong as a *correctness* habit, wrong as *scheduling*. `[Confirmed]` |
| Right approach? | **Content-fingerprint skip of expensive jobs** (compile + fixture runtime), fail-closed; keep cheap invariants always (or fingerprint them too). Predicate in `scripts/ci`; `if:` wiring in `codeql-signals.yml`. `[Evidenced]` GHA + `[Confirmed]` C-A |
| Path-filter only? | **Weaker** — “path touched” ≠ “bytes changed”; under-inclusive lists silently skip after real breaks. Acceptable only as dirty hint, not sole SoT. |
| Cache DB via `actions/cache`? | **Accelerator only after fingerprint exists** — never “cache hit ⇒ certified.” `[Evidenced]` unsigned cache / poisoning literature |
| CodeQL overlay / incremental product scanning? | **Refuse for this gate** — overlay is for `build-mode: none` product PR analysis; harness is traced `javac` fixture DB. `[Evidenced]` |
| Local vs CI today? | **Asymmetric and under-documented** — CI always runs CodeQL; `pre_pr --auto` never does (only `--actions-outage`). `spring-signals/` / `codeql/` omitted from `CODE_PATH_PREFIXES`. Fix in same epic. |
| Better choice earlier (E-CI1)? | Extracting the BC without a skip/fingerprint seam left CodeQL as the unconditional long pole (~5m compile + ~7m runtime). Should have landed predicate + job `if:` with the BC. |

**Locked product rule (proposed):** skip means *inputs to the evaluation-time SoR are byte-identical to base* — not *invariants were green* and not *cache looked warm*.

---

## 1. Confirmed seams (this repo)

| Fact | Evidence | Tier |
| --- | --- | --- |
| `ci.yml` always `uses: codeql-signals.yml` | `.github/workflows/ci.yml` | Confirmed |
| Three jobs: invariants / compile / runtime | `codeql-signals.yml` | Confirmed |
| Runtime long pole | `create-test-db.sh` → always `rm -rf` DB + traced create + wave-1 + expectations (~7m); compile+QL tests (~5m) | Confirmed (CI run inventory) |
| Stage-0 XDG content cache | `_codeql_cache_keys.py` / `_codeql_cache.py` / `_codeql_database.py` | Confirmed |
| Bash harness **does not** use Stage-0 cache | `create-db.sh` wipe+rebuild; `run.sh` wipe `OUT` | Confirmed |
| Dual packs | CI: `spring-signals/codeql/packs/*`; Stage-0: `codeql/spring-signals/` via `codeql_pack_dir()` — **not** the same SoR | Confirmed |
| Invariants ≠ evaluation SoR | `check-invariants.py` Caveat on Check 4 (meta-edge needs DB / Probe) | Confirmed |
| Policy **C-A** | Gate logic in `scripts/ci` / doc-engine; thin caller; no heredocs | Confirmed |
| `pre_pr` CodeQL only on `--actions-outage` | `build_suites` / `_append_outage_lanes` | Confirmed |
| Path-risk omits `spring-signals/`, `codeql/` | `CODE_PATH_PREFIXES` | Confirmed |
| No prior skip/fingerprint for harness | session-log / PR #90/#92: always-on gate; Stage-0 cache only | Confirmed |
| E-RUN refuse | RTS must not skip **oracle** cov cell — different predicate from skipping CodeQL when pack fingerprint unchanged | Confirmed (memo 08) |

---

## 2. External primaries (2024–2026 where possible)

| Source | Claim | Tier | Fit here |
| --- | --- | --- | --- |
| [GHA workflow `paths`](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore) | Filters whether the **workflow** runs | Evidenced | **Refuse on required CI** |
| [Required checks troubleshooting](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks) | Workflow skipped by paths → checks **Pending** (block); job skipped by `if:` → **Success** | Evidenced | Job-level `if:` only |
| [GHA `hashFiles`](https://docs.github.com/en/actions/learn-github-actions/expressions#hashfiles) | SHA-256 over matched workspace files | Evidenced | Content fingerprint shape (script preferred for unit tests) |
| [dorny/paths-filter](https://github.com/dorny/paths-filter) | Job-level path change detection | Evidenced | Optional dirty hint; not sole SoT |
| [Dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) | Cache not signed/verified; eviction | Evidenced | Accelerator ≠ SoR |
| [Cache poisoning writeup](https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache-github-actions-cache-poisoning/) | Don’t treat Actions cache as integrity boundary | Evidenced | Refuse cache-as-green |
| CodeQL overlay / incremental CLI analysis | Product PR overlay; **`build-mode: none`**; traced builds unsupported | Evidenced (product docs / action) | **Refuse** as fixture-gate substitute |
| NameRTS / T-TS / RL CI-skip papers | Test or whole-build selection | Evidenced | **Refuse as merge SoT**; pre_pr agent loops only (already E-RUN) |
| Peer-reviewed “skip CodeQL pack CI iff inputs unchanged” | — | **Unknown** | Treat as engineering under C-A, not research SoT |

---

## 3. Deep product-fit (why *these* options matter *here*)

| Option | Verdict | Elegant use (specific) |
| --- | --- | --- |
| **Workflow-level `on.paths` on `ci.yml` / required CodeQL** | **Refuse** | Would Pending-block merges or wrongly skip python-gates. |
| **Path-filter-only inside BC** | **Adopt weak / not sole** | Cheap dirty signal; fails open on missed paths; forces full run on noop touches under the filter. |
| **Content fingerprint of CI input closure** | **Embody now** | Same mental model as Stage-0 `_cache_key` / `version_hash`, applied at **harness/CI pack** boundary. Skip compile+runtime when HEAD == base over explicit corpus. |
| **Always-run invariants** | **Embody** | Seconds; catches structural pack rot even when expensive jobs skip. Does **not** replace runtime SoR (Probe caveat). |
| **`actions/cache` of fixture DB** | **Defer / optional accel** | After fingerprint exists; restore → still run expectations (or prove DB usable + assert). Never skip assertions on hit. |
| **Wire harness through Stage-0 `_codeql_runner`** | **Refuse v1** | Dual pack; runner near LOC ceiling; wrong BC coupling. |
| **CodeQL overlay / TRAP / action dependency-caching** | **Refuse for this gate** | Wrong abstraction for traced fixture pack self-test. |
| **Skip only runtime, always compile** | **Adopt as middle if corpus risk high** | Keeps ~5m QL compile/tests; saves ~7m DB. Prefer full expensive skip once fingerprint tests cover each input class. |
| **Align `pre_pr` prefixes + docs** | **Embody same tip** | Add `spring-signals/` (CI pack BC). Document CodeQL ∉ `--auto`. Optional: fingerprint gate in `--actions-outage` too. |
| **ML / soft “confidence of green”** | **Refuse** | Constitution / synthesis. |

---

## 4. Limitations of the recommended approach

1. **Incomplete fingerprint corpus = silent under-test.** Forgetting `java-signals-lib`, lockfiles, fixture Java, `deps.txt`, expectations, `setup-codeql`, or bundle SHA skips after a real break. Mitigate: characterization tests that mutate each input class and force `run`.
2. **Skip ≠ “CodeQL still healthy on this runner image.”** Java minor / OS / CodeQL bundle env outside the hash can drift. Bundle URL+SHA must be in the corpus; runner image is **Unknown** residual (accept or pin more aggressively later).
3. **Invariants-only green is not evaluation-time proof.** Document in CONTRIBUTING / workflow comment; Probe/`@RestController` recall still needs DB when fingerprint dirty.
4. **Job `if:` Success-on-skip** is correct for GHA required checks *if* the required name is a job that either runs or skips inside an always-triggered workflow — not a workflow that never starts. Confirm branch-protection check names after landing.
5. **Local/CI parity remains partial** unless `--actions-outage` / a future standard lane shares the same predicate. Do not pretend `--auto` ≡ CI CodeQL.
6. **Does not shrink Stage-0 local scan cost** — different SoR (`codeql/spring-signals/` + XDG). Out of scope.
7. **First merge after corpus change always pays full cost** — intended.

---

## 5. Better choices we should have made earlier

| When | What we did | What would have been better |
| --- | --- | --- |
| **E-CI1** (extract `codeql-signals.yml`) | Correct BC + pin ownership; **unconditional** compile+runtime | Land `scripts/ci` fingerprint predicate + job `if:` in the same tip; record runtime as evaluation-time SoR vs invariants |
| **PR #90/#92** (harness as merge gate) | Always-on fixture gate (right for correctness) | Same gate + content-addressed skip when inputs unchanged; artifact delivery already preferred over cache-as-SoR |
| **Stage-0 CodeQL cache (2026-07)** | Strong XDG keys for Python scanner | Did **not** need to unify harness with Stage-0 — but should have **named** the dual-pack split in CONTRIBUTING so CI skip wouldn’t later fingerprint the wrong tree |
| **`pre_pr` path-risk** | `.github/` in prefixes; CodeQL only in outage | Include `spring-signals/`; stop claiming “same hard suites as CI” for CodeQL under `--auto` |
| **E-RUN0** | Correctly refused RTS on **oracle** | Could have explicitly listed “CodeQL pack fingerprint skip” as a *different* allowed predicate (CI BC, not cov cell) — reduces category-error fear |

None of these reopen E-CI policy **C-A** or fail_under **98.7**. They are sequencing debts, not Spec errors.

---

## 6. Spec decisions (proposed CQ1–CQ9)

| ID | Decision |
| --- | --- |
| **CQ1** | Skip predicate lives in `scripts/ci/codeql_signals_change_gate.py` (concept-named; ≤225; complexipy ≤5). YAML only consumes outputs. |
| **CQ2** | Fingerprint corpus = CI input closure: `spring-signals/codeql/**`, `spring-signals/harness/**` (exclude `__pycache__`), `.github/workflows/codeql-signals.yml`, `.github/actions/setup-codeql/**`, `scripts/ci/setup_codeql.sh`, and bundle URL+SHA from the workflow env/pin. **Exclude** Stage-0 `codeql/spring-signals/` unless a separate sync gate is Spec’d. |
| **CQ3** | Compare fingerprint at HEAD vs merge-base / `github.event.before` / `origin/main`. Equal → `run_expensive=false`. Empty base / git error / incomplete checkout → **fail closed → run**. |
| **CQ4** | `codeql-signals-invariants` always runs. `compile` + `runtime` gated by `if: needs.gate.outputs.run_expensive == 'true'`. |
| **CQ5** | Do **not** put `on.paths` on required `ci.yml` / CodeQL workflow triggers. |
| **CQ6** | `actions/cache` of DB/compcache is **out of v1** (optional CQ-S1 after fingerprint green). Never skip assertions on cache hit. |
| **CQ7** | Align `pre_pr.CODE_PATH_PREFIXES` with `spring-signals/`; fix CONTRIBUTING “same suites as CI” for CodeQL; optionally call the same gate in `--actions-outage`. |
| **CQ8** | Characterization tests: each corpus class mutation ⇒ dirty; byte-identical base ⇒ clean; unknown base ⇒ run. |
| **CQ9** | Refuse: overlay-as-gate, ML skip, cache-as-SoR, fattening `ci.yml`, DI/`utils`, raising LOC/complexipy, skipping oracle. |

**Branch:** `cursor/e-cql-signals-gate-61f3` off `main` (new tip; not E-SCAN1).

---

## 7. Adversarial checklist (must pass before Implement Archive)

- [ ] Can a required check go **Pending** because the whole workflow was path-skipped? (Must be no.)
- [ ] Does skipping runtime while invariants pass still document Probe/DB as evaluation SoR?
- [ ] Is Stage-0 pack change correctly **ignored** by CI harness fingerprint (or explicitly Spec’d otherwise)?
- [ ] Does every corpus path have a test that flips clean→dirty?
- [ ] Does fail-closed fire when base SHA is `0000…` / missing?
- [ ] Is `ci.yml` still ≤200 and `codeql-signals.yml` ≤300 (advisory >225)?
- [ ] Are branch-protection required job names still satisfied when compile/runtime skip?
- [ ] Did we avoid claiming cache hit or invariants-only as fixture-gate green?

---

## 8. Epic E-CQL0 (Spec) → E-CQL1 (Implement)

### E-CQL0 — Spec gate (this memo)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| CQL0-1 | Record Approve **CQ1–CQ9** | Human Approve on this memo / backlog |
| CQL0-2 | Stamp quality-backlog P13 Active for Implement only after Approve | Backlog row |

### E-CQL1 — Implement (blocked on Approve)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| CQL1-1 | `scripts/ci/codeql_signals_change_gate.py` + unit/characterization tests | CQ1–CQ3, CQ8; size/complexipy |
| CQL1-2 | Gate job + `if:` on compile/runtime in `codeql-signals.yml`; invariants always | CQ4–CQ5; `check_workflow_yaml` |
| CQL1-3 | `pre_pr` prefixes + CONTRIBUTING CI layering honesty | CQ7; claims if paths cited |
| CQL1-4 | Verify: mutate fixture expectation locally → gate dirty; docs-only tip → skip receipt; `pre_pr` / workflow LOC | DoD |

### Spike (optional, after v1)

| ID | Question | Exit |
| --- | --- | --- |
| CQL-S1 | Does `actions/cache` of fixture DB cut wall-clock enough on dirty fingerprints to justify unsigned-cache ops? | Measure on 3 dirty runs; keep assertions mandatory; else refuse |

### Exit / invariants

Epic done when CQ1–CQ9 Approved, CQL1-* green, adversarial checklist checked, backlog Archive. Hard invariants: fail_under 98.7, complexipy ≤5, LOC ≤225 modules, C-A thin caller, no cache-as-SoR.

---

## 9. Explicit refuse (do not schedule)

- Workflow-level path filters on required CI  
- Restored DB / `cache-hit` as certification  
- CodeQL overlay / diff-informed as fixture-gate replacement  
- Unifying harness with Stage-0 runner in v1  
- ML / commit-message CI skip  
- Skipping python-gates or oracle because CodeQL skipped  
- Raising workflow or file LOC caps to “make room” for inline YAML logic  

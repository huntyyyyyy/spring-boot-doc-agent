---
title: Test-suite bounded contexts and parallelization
status: APPROVED — feeds E-TEST1 Implement (E-TEST0 Spec locked 2026-08-08)
date: 2026-08-08
claim tiers: Evidenced / Confirmed / Unknown
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
---

# 06 — Test-suite bounded contexts → parallel shards

Sibling to **01–05**. Those embodied DDD for *product* modules
(`coverage_measure`, PathCohesion). This segment asks the same question for the
**test topology**: why wall-clock stays serial, and what to Embody/Adopt/Refuse
before touching pytest-xdist.

---

## 1. Frame

**Symptom:** CI and local remesure run one fat `pytest tests/` process (plus an
ABI matrix without cov). Agents feel “missing parallelization.”

**Category error to refuse:** treating `-n auto` as the design. xdist amplifies
whatever shared mutable state already exists; it does not invent isolation
([pytest-xdist distribution](https://pytest-xdist.readthedocs.io/en/latest/distribution.html);
industry race write-ups). `[Evidenced]`

**Real design question:** partition the suite into **bounded test contexts**
with explicit serial quarantine, then shard CI (and only later optional
in-process xdist *inside* a shard).

---

## 2. Confirmed inventory (this repo)

Measured on tip worktree `wt-complexity-stf` (2026-08-08):

| Fact | Value | Tier |
| --- | --- | --- |
| `test_*.py` files | **225** | `[Confirmed]` |
| Top dirs | `doc_engine` 151 · `ci` 37 · `stf` 13 · `ratchets` 10 · others small | `[Confirmed]` |
| `doc_engine` name prefixes | `coverage_climb` 30 · `covering` 10 · `pipeline` 7 · **`other` 73** | `[Confirmed]` |
| Root `tests/conftest.py` | `sys.path` insert for scripts meta only — no domain fixtures | `[Confirmed]` |
| Domain / serial markers | **absent** (no `xdist_group` / `serial` / `domain_*`) | `[Confirmed]` |
| CI pytest | single `pytest tests/` per Python matrix cell; cov only on 3.11 | `[Confirmed]` `.github/workflows/ci.yml` |
| pytest-xdist | **not** in deps | `[Confirmed]` `requirements-dev.txt` / `pyproject.toml` |
| Tach | present; local “unaffected skip” — not CI SoT | `[Confirmed]` |
| `PIPELINE_ARTIFACTS*` coupling | ~10 doc_engine hits (cert / real-artifact opt-in) | `[Confirmed]` |
| Live opt-in | `DOC_ENGINE_REAL_LIVE_SCAN` skipif on OCS real-world tests | `[Confirmed]` |

**Reading:** cohesion exists as *filename prefixes* and *top-level folders*, not
as pytest collection units. The large `other` bucket is the DDD debt.

---

## 3. Primary sources (parallelism)

| Source | Claim | Tier |
| --- | --- | --- |
| [pytest-xdist distribution](https://pytest-xdist.readthedocs.io/en/latest/distribution.html) | `loadscope` / `loadfile` keep module/file on one worker; do **not** exclusive-lock shared external resources across groups | `[Evidenced]` |
| [xdist how-to (session fixtures)](https://pytest-xdist.readthedocs.io/en/stable/how-to.html) | session fixtures run **per worker**; need lock/namespace for once-global | `[Evidenced]` |
| Mergify / QASkills write-ups (2024) | scheduler ≠ isolation; use `tmp_path` / `worker_id` / per-worker namespaces | `[Evidenced]` (secondary commentary) |
| Synthesis decision **8** | xdist on climb **out of v1** | `[Confirmed]` `se-quality-synthesis` |
| Synthesis **DDD / MAO** | Embody bounded contexts; refuse unordered parallel tip writers | `[Confirmed]` |
| PathCohesion / no cross-worktree combine | Oracle cov cell must stay path-cohesive | `[Confirmed]` CONTRIBUTING + E-CM0 |

---

## 4. Alternatives

| Option | Idea | Verdict |
| --- | --- | --- |
| **A. Marker + CI path shards first** | Define domains; CI jobs `pytest -m domain_X` or path globs; serial job for quarantine | **Adopt (v1)** |
| **B. Big-bang `tests/<bc>/` move** | Physical DDD layout in one PR | **Refuse** as first move (claim/path churn; Tach noise) · **Adopt gradual** after markers |
| **C. Global `-n auto` on `tests/`** | Fastest wall-clock attempt | **Refuse v1** until serial quarantine proven |
| **D. xdist only inside climb** | Sensor loop parallel | **Defer** (decision **8**); after domains |
| **E. Tach as CI gate** | Skip unaffected in Actions | **Refuse as SoT** · local accelerator OK |
| **F. Coverage matrix cells as shards** | Split cov collection across jobs then combine | **Refuse** (cross-job combine = PathCohesion hazard) |

---

## 5. Embody / Adopt / Refuse (suite topology)

| Item | Stance |
| --- | --- |
| Test BCs aligned to product concepts (Stage-0, pipeline, schemas, ci-meta, …) | **Embody** |
| Markers + CI shards before mass moves / before global xdist | **Adopt** |
| Explicit `serial` quarantine (e2e cert wiring, kitchen_sink, editable-root thrash) | **Embody** |
| Oracle 3.11 cov cell remains **one process** writing `coverage.xml` | **Embody** (E-CM / policy **16-A**) |
| Global xdist on full suite in v1 | **Refuse** |
| Cross-job `coverage combine` for shard speed | **Refuse** |
| Tach as merge SoT | **Refuse** |
| Climb xdist | **Defer** (decision **8**) |
| Parallel tip thrash on baselines / fail_under while reshaping tests | **Refuse** |

---

## 6. Proposed bounded test contexts (draft names)

Stable **marker** names (directory moves optional later):

| Marker / BC | Intent | Parallel default |
| --- | --- | --- |
| `domain_schemas` | artifact schemas, serde, validators shape | parallel-safe |
| `domain_stage0` | signals, covering, gap_probe, facts/ETL, absences | parallel-safe if tmp-isolated |
| `domain_pipeline` | partition, capacity, stages shape, local_runner units | mostly parallel; some serial |
| `domain_compliance` | compliance profiles, cert report units | parallel-safe |
| `domain_ci_meta` | `tests/ci`, ratchets, claims helpers | parallel-safe |
| `domain_adapters` | `tests/adapters` | parallel-safe |
| `domain_stf` | `tests/stf` | parallel-safe |
| `domain_climb_sensor` | `test_coverage_climb_*` | parallel-safe; **not** oracle proof |
| `domain_integration` | kitchen_sink, certified e2e wiring, PIPELINE_ARTIFACTS opt-in | **serial** |
| `domain_live_optin` | real-world OCS / live scan | opt-in / skip; never default CI wall |

Unassigned `other` files must be labeled in Spec tickets — unlabeled stays
**serial** until classified (`unknown → serial` ratchet).

---

## 7. Open measurements `[Unknown]` until spike

- Wall-clock share of `domain_climb_sensor` vs rest on 3.11 cov cell.
- Flake rate under `loadfile` inside one non-cov ABI shard (spike only).
- Whether `tests/support` helpers assume process-global caches.

---

## 8. Link forward

Design Spec gate: `docs/design/test-suite-parallel-domains-design-2026-08-08.md`  
Backlog: E-TEST0 → E-TEST1 (markers/shards) → optional E-TEST2 (xdist-in-shard).

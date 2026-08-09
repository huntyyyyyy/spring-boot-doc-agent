---
category: Test suite / bounded contexts / CI parallelization
status: APPROVED — SPEC GATE E-TEST0 (2026-08-08)
research date: 2026-08-08
approved_decisions: T1-T18
artifact_policy: T-A
claim tiers: Evidenced / Confirmed / Unknown
research: docs/research/modularity/06-test-suite-bounded-contexts-parallel.md
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
---

# Design memo: test-suite bounded contexts → CI shards

> **APPROVED — SPEC GATE E-TEST0 (2026-08-08)**
>
> Principal / implementer chat recorded **Approve** of decisions **T1–T18**
> with parallelization policy **T-A** (CI marker/path shards before suite-wide
> xdist). Implement epic **E-TEST1** is unblocked as the next single stream.
> Do not enable suite-wide `-n auto`, cross-job `coverage combine`, or climb
> xdist without E-TEST2 spikes. Does not reopen E-CM **1–31** or policy **16-A**.

**Spec record**

| Field | Value |
| --- | --- |
| Decisions | **T1–T18** Approved |
| Policy **T** | **T-A** — CI marker/path shards **before** in-process xdist |
| Branch / PR | `wave1-gates-untrusted-tree-hygiene` / [#94](https://github.com/huntyyyyyy/spring-boot-doc-agent/pull/94) |
| Research | [`docs/research/modularity/06-test-suite-bounded-contexts-parallel.md`](../research/06-test-suite-bounded-contexts-parallel.md) |
| Backlog | [`docs/research/quality-backlog.md`](../research/quality-backlog.md) |

---

## 1. Problem

Wall-clock and agent feedback are gated by a **single fat collection unit**
(`pytest tests/`), while product DDD already insists on concept modules.
Tests mostly did **LOC splits** (`test_pipeline_stages_*.py`, climb batches),
not **bounded-context partitions** that CI can run concurrently.

| Defect | Evidence |
| --- | --- |
| One pytest invocation owns the suite | `[Confirmed]` CI `pytest tests/` |
| No domain/serial markers | `[Confirmed]` suite scan |
| Flat `doc_engine` bag (~151 files; 73 `other`) | `[Confirmed]` inventory |
| Global xdist would hit shared env/artifact coupling | `[Confirmed]` `PIPELINE_ARTIFACTS*`; `[Evidenced]` xdist docs |
| Oracle cov cell must stay one cohesive writer | `[Confirmed]` E-CM0 / PathCohesion / policy **16-A** |

**Root cause:** missing test BCs → no safe shard boundaries → parallelization
looks like “add `-n auto`” when the missing design is **domain isolation**.

---

## 2. Research summary

See segment **06**. Short form:

- **Embody** DDD for tests; **Adopt** marker+CI shards first (**T-A**).
- **Refuse** global xdist v1; **Refuse** cross-job coverage combine.
- **Defer** climb xdist (synthesis decision **8**).
- Unlabeled tests default **serial** until classified.

---

## 3. Policy **T** — locked **T-A**

| Option | Meaning |
| --- | --- |
| **T-A** (locked) | **Shard-first:** pytest markers + CI jobs by domain; serial job for `domain_integration` + unclassified; **no** suite-wide xdist until shards are green. Optional later: xdist *inside* one non-oracle shard (E-TEST2). |
| **T-B** | **xdist-first** — **Rejected** at Spec gate |
| **T-C** | **Directory-first** mass-move — **Rejected** as first move; gradual moves still allowed after markers (**T6**) |

---

## 4. Decisions (**T1–T18**) — Approved

### Topology (T1–T7)

1. **T1.** Test bounded contexts use the marker vocabulary in research §6
   (`domain_schemas`, `domain_stage0`, `domain_pipeline`, `domain_compliance`,
   `domain_ci_meta`, `domain_adapters`, `domain_stf`, `domain_climb_sensor`,
   `domain_integration`, `domain_live_optin`).
2. **T2.** Every new `test_*.py` must declare exactly one `domain_*` marker
   (CI check or ratchet — Implement epic).
3. **T3.** Files without a domain marker are treated as **`serial` / unclassified**
   until labeled (fail-closed for parallel jobs).
4. **T4.** `domain_integration` and unclassified run only in the **serial** CI job.
5. **T5.** `domain_live_optin` stays skip-gated; never on the default PR critical path.
6. **T6.** Physical `tests/<bc>/` moves are **optional and gradual** after markers;
   not a Spec prerequisite for shards.
7. **T7.** `tests/support` stays shared kernel (fixtures/helpers), not a “utils bag”
   for product code; no new grab-bag test modules.

### Parallelization (T8–T12)

8. **T8.** Policy **T-A**: CI path/marker shards before suite-wide xdist.
9. **T9.** Oracle **3.11** coverage cell remains a **single process** writing
   `coverage.xml` (may still *select* domains via markers, but one writer).
10. **T10.** ABI matrix cells (3.10/3.12, no cov) **may** shard by domain in
    parallel GitHub jobs.
11. **T11.** Suite-wide `pytest -n auto` on `tests/` is **out of E-TEST1**.
12. **T12.** Climb-mode xdist remains **deferred** (synthesis **8**); not unlocked
    by E-TEST0 alone.

### SoT / process (T13–T18)

13. **T13.** Tach remains a **local** accelerator; never the merge SoT.
14. **T14.** No cross-job / cross-worktree `coverage combine` to speed shards.
15. **T15.** SDD one-stream: Spec (this memo) → Implement (E-TEST1) → Verify →
    Archive; no parallel tip thrash on CI yaml + baselines.
16. **T16.** Certified local_runner gate keeps `gate_id=test_pipeline_stages` but
    may collect split modules (already landed); domain marker =
    `domain_pipeline` (or integration if env-coupled).
17. **T17.** Size/complexipy/fail_under **98.7** invariants unchanged.
18. **T18.** Explicit refuse: mesh/Backstage test dashboards, PIT-as-shard-oracle,
    LLM-judge suite partitioning.

---

## 5. Adversarial checklist (review packet)

- [ ] Does any proposed shard write `coverage.xml` besides the 3.11 oracle cell?
- [ ] Can two parallel jobs mutate the same fixture checkout or editable install?
- [ ] Are kitchen_sink / certified e2e forced serial?
- [ ] Does marker ratchet fail closed (unlabeled ≠ parallel)?
- [ ] Is Tach accidentally wired as required CI?
- [ ] Does E-TEST reopen climb fail_under or policy **16-A**? (must not)

---

## 6. Epic E-TEST0 — Spec gate — **DONE**

| ID | Ticket | Est | Acceptance |
| --- | --- | --- | --- |
| TEST0-1 | Record Approve of **T1–T18** + **T-A** | 0.5d | **Done** — status APPROVED 2026-08-08 |
| TEST0-2 | BC ownership table (prefix → `domain_*`) | 0.5d | **Done** — §11 appendix |

**Exit E-TEST0:** Complete. Next stream = **E-TEST1**.

---

## 7. Epic E-TEST1 — Markers + CI shards (unblocked)

| ID | Ticket | Est | Acceptance |
| --- | --- | --- | --- |
| TEST1-1 | Register markers in `pyproject.toml`; document in CONTRIBUTING | 0.5d | `pytest --markers` lists domains; claims paths OK |
| TEST1-2 | Classify ``tests/doc_engine`` to **meeting rate ≥98.7** (same floor as Cover%); debt inventory = ``domain_unclassified`` only — once reclassified, a module leaves that inventory (gap-average analogy) | 1–2d | `test_domain_markers_check` prints meeting% and debt count; meeting ≥98.7 |
| TEST1-3 | CI: parallel jobs for safe domains on ABI cells; serial job for integration/unclassified | 1d | workflow green; wall-clock note in PR |
| TEST1-4 | Ratchet: new test file without `domain_*` fails check (hermetic) | 0.5d | red test / ci script |
| TEST1-5 | Keep 3.11 oracle cov as single writer (markers optional for selection only) | 0.5d | still one `coverage.xml`; PathCohesion OK |

**Exit E-TEST1:** Sharded ABI CI + marker ratchet; no suite-wide xdist.

---

## 8. Epic E-TEST2 — Optional in-shard xdist (spikes)

| ID | Spike / ticket | Exit criterion |
| --- | --- | --- |
| S-TEST2-1 | Wall-clock profile: climb_sensor vs stage0 vs pipeline | Numbers in research note |
| S-TEST2-2 | xdist `loadfile` inside one **non-oracle** shard only | Flake budget agreed; worker_id / tmp isolation |
| TEST2-1 | If spike OK: pin pytest-xdist; enable on that shard only | CI green N consecutive runs |

**Refuse until spikes:** global `-n` on oracle cell.

---

## 9. Invariants (constitution)

- `fail_under=98.7` · complexipy ≤5 · LOC ≤225 · no utils grab-bag  
- Policy **16-A** climb XML ≠ oracle XML  
- SDD one-stream; no unordered multi-writer SoT tip  

---

## 10. Approval record

```text
E-TEST0 Spec: Approve T1–T18 with policy T-A.
Recorded: 2026-08-08 (principal / implementer chat).
```

---

## 11. Appendix — BC ownership (prefix / path → marker)

Initial map for E-TEST1 labeling (refine in TEST1-2; unknowns → serial):

| Marker | Seed paths / prefixes |
| --- | --- |
| `domain_schemas` | `test_artifact_*`, `test_*schema*`, validators shape under doc_engine |
| `domain_stage0` | `test_gap_probe*`, `test_covering*`, `test_*etl*`, `test_*signal*`, `test_absence_*`, `test_facts_*`, `tests/spring_signals/` |
| `domain_pipeline` | `test_pipeline_*`, `test_partition_*`, `test_capacity_*`, `test_local_runner*`, `test_build_cross_group*`, `test_context_packet*` |
| `domain_compliance` | `test_compliance*`, cert report units (non-e2e) |
| `domain_ci_meta` | `tests/ci/`, `tests/ratchets/`, `tests/coverage/` |
| `domain_adapters` | `tests/adapters/` |
| `domain_stf` | `tests/stf/` |
| `domain_climb_sensor` | `test_coverage_climb_*` |
| `domain_integration` | `test_kitchen_sink*`, certified e2e / `PIPELINE_ARTIFACTS*` opt-in, enterprise kitchen |
| `domain_live_optin` | `*_ocs_real_world*`, live-scan skipif modules |
| unclassified → serial | Remaining `doc_engine` `other` until labeled |

---
title: SE quality synthesis — dual-mode, taxonomy, metrics, frameworks, dynamics
status: PRINCIPAL MEMO — merge of research segments 01–05
research date: 2026-08-08
base_sha: 5eaac2ac20fbe2c4aebd2652c64a58defbcc10a7
claim tiers: Evidenced / Confirmed / Unknown
sources:
  - docs/research/coverage-quality/01-coverage-oracle-climb-solid.md
  - docs/research/process/02-foundational-agentic-se-2026.md
  - docs/research/coverage-quality/03-scientific-dimensions-metrics.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/process/05-dynamics-neuromorphic.md
supersedes:
  - docs/research/archive/_wip-coverage-design-audit.md
related:
  - docs/design/coverage-measure-modes-design-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - weaken fail_under, complexipy ≤5, or size ≤225
  - reopen policy 16-A or fuzzy/PID green after Spec gate
spec_gate: APPROVED E-CM0 (2026-08-08) — decisions 1-31 + policy 16-A
---

# Principal memo: SE quality synthesis (2026-08-08)

Consolidated Embody / Adopt / Refuse, amended decisions **1–31**, and claim-tiered
verdicts for **spring-boot-doc-agent**: a Python CLI / agentic Spring-doc product with
deterministic gates. Not a K8s microservice farm. Spec gate **E-CM0** recorded
**Approve** of **1–31** with policy **16-A** in the design memo; dual-mode lands
under **E-CM1** only.

**Claim tiers:** `[Evidenced]` primary paper/docs · `[Confirmed]` local seams ·
`[Unknown]` missing ID, hype transfer, or product choice still open.

**Sibling SoTs (do not invent past them):** 01 coverage · 02 taxonomy · 03 metrics ·
04 frameworks · 05 dynamics.

---

## 1. Executive verdict

| Question | Answer |
| --- | --- |
| Approve dual-mode decisions **1–12** alone? | **No.** |
| Approve after amendments? | **Yes — approve 1–31** (or an explicit subset that still includes **13–17, 19–21, 25–26, 29**). |
| Implement dual-mode now? | **No** — design confirmation first; then one-stream Spec→Impl→Verify. |
| Product category change (mesh/ECS/Backstage/SNN)? | **Refuse.** |

**Minimum bar before climb/oracle code:**

1. Strategy + naming + complexipy ≤5 (**13–15**).
2. Promotion ban + climb artifact policy A or B recorded (**16**).
3. Layer binding: climb ≠ floor (**17**); banner (**11**).
4. Hard predicates stay boolean — no PID/fuzzy green (**25**).
5. SDD one-stream + no ungated self-evolution + LLM-judge ≠ fail_under (**19–21**).

---

## 2. Source verification (hype filter)

| Claimed label | Result | Tier |
| --- | --- | --- |
| CoverUp arXiv:2403.16218 | Exists — iterate missing segments; final whole-suite check | `[Evidenced]` |
| ChaCo arXiv:2601.10942 | Exists — patch-scoped ≠ whole-repo floor | `[Evidenced]` |
| pytest-cov `--cov` / fail_under | Overrides source; fail_under on **reported** measured total | `[Evidenced]` |
| SDD process arXiv:2606.04967 | Exists — Spec Kit / OpenSpec / Spec Kitty taxonomy | `[Evidenced]` |
| Self-evolving agents arXiv:2608.03392 | Exists — survey; SICA/SIFT labels not paper title objects | `[Evidenced]` / SICA·SIFT `[Unknown]` |
| Issue resolution arXiv:2512.22256 | Exists — validate/select bind acceptance | `[Evidenced]` |
| Log smells arXiv:2412.09284 | Exists — nine smells | `[Evidenced]` |
| MSR-LM arXiv:2604.00787 | Exists — LM-in-MSR survey | `[Evidenced]` |
| Semantic density 2604.07502 / 2604.17659 | Exist — prefer descriptive tokens; compression can raise cost | `[Evidenced]` |
| Green AI arXiv:1907.10597 | Exists — efficiency as criterion | `[Evidenced]` |
| SpikeSlicer arXiv:2410.02249 | Exists — DVS/SNN CV; **not** a CI gate primitive | `[Evidenced]` domain / refuse transfer |
| PID edge scaling arXiv:2109.02514 | Exists — K8s queue control; **not** coverage floor | `[Evidenced]` domain / refuse transfer |
| DeepWiki “crupig” / “pierpaolo28” | **Not found** — use openevals for judge; FDE = industry role only | `[Unknown]` |
| Thesirix cartography | Profile mindmap only | Vocabulary, not architecture SoT |

---

## 3. Oracle vs climb (Deterministic vs Probabilistic)

```text
DETERMINISTIC (SoT / SLO)              PROBABILISTIC (feedback)
─────────────────────────              ────────────────────────
mode=oracle full suite                 mode=climb scoped --cov
fail_under=98.7 (boolean)              Cover% / missing for scope
PathCohesionGuard                      guides next edit batch
CI 3.11 cov cell                       never claims repo floor
coverage.xml (authoritative)           gap-average (derived view)
diff-cover new-code gate               LLM plan / patch proposals
complexipy / size / claims             LLM-as-judge (advisory only)
```

**pytest-cov trap `[Evidenced]`:** scoped `--cov` + `--cov-fail-under=98.7` is a
*different predicate* than whole-repo 98.7. Unlabeled reuse = hidden SoT → **Refuse**.

**DDIA `[Confirmed]` local north-star + Kleppmann dual-write:** only cohesive oracle XML
may assert floor; climb/gap are rebuildable derived views; never dual-write climb into
oracle filename without policy **16**.

---

## 4. Master Embody / Adopt / Refuse

### 4.1 Coverage & SoT (segment 01)

| Item | Stance |
| --- | --- |
| Oracle = whole-repo SoT / SLO-like floor | **Embody** policy · **Adopt** labeled `--mode oracle` |
| Climb = scoped accelerator (CoverUp-shaped) | **Adopt** |
| Scoped Cover% as proof of 98.7 | **Refuse** |
| Climb applying whole-repo fail_under | **Refuse** |
| Gap-average rewriting targeting SoT | **Refuse** (derived only) |
| diff-cover as below-floor climb driver | **Refuse** as primary · **Embody** as new-code gate |
| PathCohesion + single-writer wipe | **Embody** |
| Cross-worktree combine | **Refuse** |
| xdist on climb in v1 | **Refuse (defer)** |
| Strategy/polymorphism for modes | **Adopt** |
| Single-letter mode vars | **Refuse** |
| Weakening CI 98.7 / cov on 3.10+3.12 | **Refuse** |
| Climb artifact policy A or B | **Adopt (choose one before impl)** `[Unknown]` which |

### 4.2 Taxonomy layers (segment 02)

| Item | Stance |
| --- | --- |
| µsvc / EDA / serverless / CQRS as product infra | **Refuse** · analogies OK |
| Lightweight SDD (OpenSpec-style deltas) | **Adopt** |
| Spec Kit WorkflowEngine as runtime | **Refuse** (S-STF-A) |
| Ungated self-evolving scaffolds | **Refuse** |
| Issue-resolution Plan-Act-Verify | **Embody** partial · Verify = deterministic gates |
| Log-smell CI before incident seed | **Refuse** parallel gate · **Adopt** selective hygiene |
| LLM-as-judge as SoT | **Refuse** |
| FDE / enterprise RAG as core | **Refuse-as-core** / DeepWiki handle `[Unknown]` |
| Hermetic Stage-0 / MSR-like fixtures | **Embody** · LM classifiers as Stage-0 SoT **Refuse** |

### 4.3 Metrics (segment 03)

| Item | Stance |
| --- | --- |
| complexipy ≤5 | **Embody** · **Refuse** raising to land features |
| Size ≤225 / stmts ≤50 (soft 150/20) | **Embody** |
| Oracle + diff-cover 98.7 | **Embody** boolean setpoints |
| McCabe as sole complexity SoT | **Refuse** |
| Ca/Ce / LCOM numeric CI cathedral | **Refuse** v1 |
| Error-budget burn under 98.7 | **Refuse** |
| SDE CI metric | **Refuse** v1 · **Embody** naming culture |
| Green AI cheap wins (3.11-only cov) | **Embody** · carbon APIs block merges **Refuse** v1 |
| Recall@K / packet freshness as Cover% SoT | **Refuse** |
| Climb iterations as process metric | **Adopt** (not floor) |

### 4.4 Frameworks (segment 04)

| Framework | Stance |
| --- | --- |
| DDD bounded contexts / concept modules | **Embody / deepen** |
| Hexagonal ports for measure modes | **Adopt** |
| Vertical slicing vs type layers / utils | **Embody** · utils grab-bag **Refuse** |
| DOD / ECS | **Refuse** |
| WASM / Rust in-tree hot paths | **Refuse by default** |
| Green-Ops / carbon-aware CI | **Optional later** |
| Golden path CLI (no Backstage) | **Embody** |
| GitOps controllers (Argo/Flux) | **Refuse** as deps · git-as-SoT analogy OK |
| Service mesh | **Refuse** |
| MAO unordered parallel tip | **Refuse** · gated single-writer OK |
| RAG embedding as citation/coverage SoT | **Refuse** |

### 4.5 Dynamics (segment 05)

| Idea | Stance |
| --- | --- |
| Neuromorphic / SNN / DVS runtime | **Refuse** |
| Saliency → debounce oracle remesure | **Adopt** docs/process · **Embody** decision 5 |
| Hysteresis on targeting / soft bands | **Adopt** |
| Fuzzy “confidence of green” for oracle | **Refuse** |
| SoA rewrite of domain graphs | **Refuse** |
| PID as coverage-floor controller | **Refuse** |
| Simple rate caps before PID concurrency | **Adopt** if needed later |

---

## 5. Unified decision list (approve set)

### Dual-mode skeleton (1–12) — from design memo / segment 01

1. One entry point: `doc-engine coverage-measure --mode oracle|climb` (default `oracle`).
2. Climb scope: `--scope <package>` → `--cov=<scope>`; optional pytest path narrowing.
3. Climb must not apply whole-repo `fail_under=98.7` (optional `--climb-floor` advisory only).
4. Gap inventory derived from last cohesive **oracle** XML only.
5. Oracle cadence: remesure after climb batch / before PR / stale inventory — not every edit.
6. PathCohesionGuard + wipe for both modes; forbid cross-worktree combine.
7. Do not weaken CI 98.7 on 3.11; no cov cells on 3.10/3.12.
8. xdist out of v1; optional climb-only follow-up.
9. diff-cover unchanged new-code gate; not climb inventory.
10. CLI thin facade; no utils bag if >225 LOC.
11. Climb banner: `mode=climb (not CI oracle)`.
12. Land on wave1 tip that owns MeasureRun/PathCohesion — no SoT-forking side branch.

### Quality bar (13–16) — segment 01

13. **OCP / polymorphism:** `MeasureMode.ORACLE|CLIMB` strategies; shared wipe + PathCohesion; no if/elif god.
14. **Naming bar:** domain vocabulary; refuse `m`/`o`/`c` and abbreviation theater.
15. **complexipy ≤5:** no mode-boolean soup; size ≤225 still binds new modules.
16. **Promotion ban + artifact policy:** choose **(A)** distinct climb XML path **or** **(B)** climb refuses writing `coverage.xml` — banner alone insufficient.

### Taxonomy / layers (17, 19–21) — segment 02

17. **Layer binding:** oracle = only coverage SoT/SLO; climb = verification-loop feedback; climb exit ≠ floor proof.
19. **No ungated self-evolution** of CONSTRAINTS / baselines / fail_under without human + claims/ratchet.
20. **LLM-as-judge ≠ fail_under.**
21. **SDD one-stream** Spec→Implement→Verify; prefer OpenSpec deltas; refuse Spec Kit WorkflowEngine runtime.

### Frameworks (18, 22–23) — segment 04

18. **Bounded context:** oracle/climb share PathCohesion; diverge via hexagonal strategies — not ECS, not second top-level BC.
22. **Refuse list:** DOD/ECS, service mesh, Backstage-required IDP, GitOps controllers, WASM/Rust hot paths unless profiled exception.
23. **Green-Ops:** keep cov-only-3.11; carbon-aware CI optional; prefer climb scoping for local energy/time.

### Metrics (24, 29–31) — segment 03

24. **Semantic density:** descriptive names + vertical modules; no SDE CI metric in v1.
29. **Metric layering:** only CONTRIBUTING hard gates are merge SoT; climb/gap/judge/Recall@K/carbon/Ca·Ce are sensors — never silent promotions.
30. **Complexity SoT:** complexipy ≤5 remains; McCabe/C901 optional/soft only.
31. **Environmental accounting:** keep 3.11-only cov; never block oracle correctness on carbon APIs in v1.

### Dynamics (25–28) — segment 05

25. **Hard predicates stay hard:** no PID/fuzzy/“confidence of green” softening of fail_under.
26. **Saliency for cadence:** debounce full oracle remesure; salient triggers only (aligns **5**).
27. **Hysteresis only on advisory/targeting** — never on oracle pass/fail.
28. **SoA / neuromorphic / PID theater refused** for domain models and coverage SoT in v1; simple rate caps before any concurrency PID.

*(Decision **18** also owned by frameworks; **21** restated by frameworks — single meaning.)*

---

## 6. Principle scorecard (dual-mode after amendments)

| Concern | Score after 1–31 |
| --- | --- |
| DDIA SoR vs derived / single-writer | **Pass** if **16** records A or B |
| SOLID / OCP / DIP | **Pass** with **13**, **18** |
| DRY (correct abstraction) | **Pass** — share wipe/cohesion, not fail_under across modes |
| complexipy ≤5 / size | **Pass** with **15**, **10** |
| Naming / semantic density | **Pass** with **14**, **24** |
| Agentic envelope | **Pass** with **17**, **19–21**, **25** |
| No hype transfer (SNN/PID/ECS/mesh) | **Pass** with **22**, **28** |

---

## 7. SDD sequencing (one-at-a-time)

From arXiv:2606.04967 + local S-STF ADRs `[Confirmed]`:

1. **Spec** — this memo + design memo decisions approved by human.
2. **Implement** — single stream; LOC/size first if ratchet fails; dual-mode only after approve.
3. **Verify** — deterministic gates; remesure oracle before PR.
4. **Archive** — CONTRIBUTING Oracle-vs-Climb table; session-log only if steering moves.

Ordered next actions: [`quality-backlog.md`](quality-backlog.md).

---

## 8. References (anchors only)

See sibling segments for full bibliographies. Primary merges: CoverUp 2403.16218; ChaCo 2601.10942; Macedo 2606.04967; Zhou 2608.03392; Jiang/Lo/Liu 2512.22256; Saarimäki 2412.09284; Romero-Arjona 2604.00787; Ustynov 2604.07502; SDE 2604.17659; Schwartz Green AI 1907.10597; SpikeSlicer 2410.02249; PID edge 2109.02514; pytest-cov docs; DeepWiki openevals + pytest-cov controllers; CONTRIBUTING gates; `coverage_measure.py` / PathCohesionGuard.

---

## 9. WIP status

`docs/research/archive/_wip-coverage-design-audit.md` is **superseded** by this file + the five
segments. Keep only as historical dump or delete in a follow-up docs commit.

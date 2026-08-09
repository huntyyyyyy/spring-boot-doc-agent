---
title: Pipeline / Stage-0 modularity via ports & vertical slices (2026)
status: E-MOD0 APPROVED · E-MOD1–2 LANDED · E-MOD3 see research 13 (2026-08-09)
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine — pipeline + Stage-0 tools BCs
related:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/04-implementation-frameworks.md
  - docs/research/quality-backlog.md
  - docs/research/10-kitchen-harness-modernization-2026.md
  - docs/product-architecture.md
do_not:
  - weaken fail_under 98.7, complexipy ≤5, LOC ≤225
  - introduce DI containers (injector / Guice-style)
  - create utils/ grab-bag modules
  - adopt mesh / Backstage / Spec Kit WorkflowEngine as runtime
  - raise FILE_LOC_HARD (225) or complexipy caps
  - rewrite all Stage-0 tools in one tip
spec_gate: APPROVED E-MOD0 (2026-08-09) — M1–M12 (plan accept)
---

# Principal memo: pipeline / Stage-0 modularity (ports & vertical slices)

**Question:** After E-KH1, is the next product stream another CI *sensor* epic — or
paying down grandfathered LOC giants with hexagonal ports and concept modules?

**Product fit filter (segment 04 / product-architecture):** one Python CLI hosting
several DDD bounded contexts (pipeline, scanning/Stage-0 tools, query, ci). Not
microservices, not an IDP, not a Spec Kit runtime.

**Claim tiers:** `[Evidenced]` primary docs/paper · `[Confirmed]` this repo ·
`[Unknown]` open product choice.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| What is the product? | **One Python CLI** with several DDD BCs — not a service mesh / plugin marketplace `[Confirmed]` (`docs/product-architecture.md`). |
| Next single stream? | **E-MOD** — modularity debt paydown. **E-MOD1** = `mock_stages` first; **E-MOD2** = Stage-0 tools after MOD1 exits. |
| Another CI sensor epic (E-UX2 / E-QA3 / E-RUN*)? | **Defer** until MOD wave1 exits — sensors are not “build the rest of the product.” |
| Revolutionary DI container / utils layer? | **Refuse.** |
| How do we split without weakening gates? | Spike **MOD-S1**: split ≤225 + façade + `size_ratchet --update` in the **same commit**; never raise `FILE_LOC_HARD`. |

**Management framing:** Embody DDD deepen + vertical slices; Adopt Protocol/Strategy
at BC edges; Spec → Implement → Verify → Archive; one tip writer.

---

## 1. Evidence inventory

| Claim | Tier | Source |
| --- | --- | --- |
| `mock_stages.py` LOC **851** (baselined offender) | Confirmed | `wc -l` + `scripts/ratchets/size_baseline.json` |
| `capacity_preflight.py` LOC **856** | Confirmed | same |
| `spring_drift_check.py` LOC **695** | Confirmed | same |
| `partition_repo.py` LOC **653** | Confirmed | same |
| Size ratchet **grandfathers** offenders; growth blocked; hard cap remains 225 | Confirmed | `python -m doc_engine.ci.size_ratchet` (`file_loc_hard=225`) |
| Existing ports: `StageExecutor`, `Scanner`, `MeasureStrategy`, `PacketProvider` | Confirmed | `pipeline/executor.py`, `core/protocols.py`, `ci/coverage_measure_modes.py`, `query/protocols.py` |
| Kitchen tip E-KH1 landed; fixture/ports pattern is product-adjacent precedent | Confirmed | research 10; PR #106 |
| Hexagonal + vertical slicing stance for this CLI | Evidenced / Confirmed | research 04 Embody/Adopt/Refuse; synthesis |

**Read:** size grandfathering is intentional debt, not a license to grow. Remediation
is Spec-gated split — not raising caps.

---

## 2. Embody / Adopt / Refuse → M1–M12 (APPROVED)

| ID | Decision | Stance |
| --- | --- | --- |
| M1 | Product stays one Python CLI hosting **several DDD BCs** (pipeline, scanning/Stage-0 tools, query, ci) — not microservices | Embody |
| M2 | **Hexagonal:** core ports = `Protocol`s at BC edges; adapters = CLI argv, filesystem, pytest, MCP | Adopt / deepen |
| M3 | **OCP:** new stage / scanner / gate via Strategy/registry registration — not god-module if/elif growth | Adopt |
| M4 | **Vertical / concept modules** under existing packages (`pipeline/`, `tools/`, `scanning/`) — **Refuse** `utils/` | Embody |
| M5 | **DIP:** constructors / explicit params at boundaries; **Refuse** DI containers (injector/Guice) and service locator | Embody / Refuse |
| M6 | Creational: **Factory/Builder** only where object graphs are multi-step (signals, preflight reports); no Abstract Factory zoo | Adopt carefully |
| M7 | Structural: keep **Facade** (thin CLI), **Adapter** (tool invoke / MCP); Composite only if stage graphs earn it | Embody |
| M8 | Behavioral: **Strategy** (stages, scanners, measure modes already); Template Method for shared gate runners; CoR only if ordered handler pipeline is real | Adopt |
| M9 | **DDIA:** preserve fault≠failure / characterization oracles; SoT vs sensor vocabulary unchanged; single-writer PathCohesion for coverage artifacts | Embody |
| M10 | Size: split until **≤225 LOC**; update size baseline as offenders disappear (no silent raise of hard cap) | Adopt (MOD-S1) |
| M11 | Dependencies: stdlib + pinned tools; typing **Protocol**; lazy import only for optional heavy tools — not plugin marketplace | Embody |
| M12 | One remediation tip at a time; no parallel SoT thrash on baseline + module moves | Embody (SDD) |

Human Approve = plan accept of M1–M12 (2026-08-09). `[Confirmed]` Spec gate.

---

## 3. Spike MOD-S1 — Size-baseline split procedure (authoritative)

**Question:** Does splitting a grandfathered file require baseline surgery in the
same commit? **Yes.**

| Step | Action | Gate |
| --- | --- | --- |
| 1 | Measure current tree: `python -m doc_engine.ci.size_ratchet` | Record offender list |
| 2 | Split grandfathered file into **concept modules each ≤225 LOC**; keep a **stable façade** module path that re-exports the public API | New files >225 fail hard immediately |
| 3 | **Same commit:** `python -m doc_engine.ci.size_ratchet --update` so baseline drops removed/shrunk offender paths and records new files | Never raise `FILE_LOC_HARD` (225) or weaken hard policy |
| 4 | Growing a baselined file still fails; **shrinking is allowed** and should be committed via `--update` | complexipy ≤5; fail_under 98.7 untouched |

Policy **16-A** and oracle Cover% are orthogonal — modularity tips must not conflate
climb sensors with the whole-repo floor.

---

## 4. Appendix A — E-MOD1 seam map (`mock_stages`, no behavior change)

Target modules by concept (all under `src/doc_engine/pipeline/`):

| Module | Responsibility |
| --- | --- |
| `mock_stage_constants.py` | `EM`, `STAGE_*`, `DOC_ORDER`, `DOC_BUCKETS`, phrasing / bucket maps |
| `mock_stage_io.py` | `_read_json` / `_write_json` / `_write_text` / `find_existing_readme` |
| `mock_citations.py` | `load_citations` / `pick` / evidenced (and related) tags |
| `mock_todo_sweep.py` | `sweep_todos` (+ walk helpers) |
| `mock_file_summaries.py` | `mock_file_summaries` cluster |
| `mock_architecture_stage.py` | `mock_architecture` cluster (name avoids clash with other architecture modules) |
| `mock_gap_interview.py` | `mock_gap_and_interview` |
| `mock_docs_stage.py` | `mock_docs` |
| `mock_stage_strategy.py` | `Protocol` `MockStageStrategy` + registry `stage_key → strategy` |
| `mock_stages.py` | **Thin façade** re-exports (stable import path for kitchen / `run_chain` / tests) |

**E-MOD1 order:** map seams → introduce Strategy Protocol + registry → vertical split
→ Verify (kitchen/pipeline domains, size/complexipy, oracle 3.11) → Archive P11.1.

`[Unknown]` until implement: exact public symbol set kitchen imports after façade thin —
characterization tests are the oracle.

---

## 5. Epic tickets

| Epic | Status | Goal / exit |
| --- | --- | --- |
| **E-MOD0** | **Done** (2026-08-09) | Spec M1–M12 Approve; this memo + backlog P11 |
| **E-MOD1** | **Done** (2026-08-09) | `mock_stages` → ≤225 concept modules + Strategy; façade stable; gates green |
| **E-MOD2** | **Done** (2026-08-09) | `capacity_preflight` → `spring_drift_check` / tier2 → `partition_repo`; CLI behavior unchanged |
| **E-MOD3** | **Active** — see [`13-tools-wave2-modularity-2026.md`](13-tools-wave2-modularity-2026.md) | `run_manifest` + `citation_coverage` tools wave 2 |

Deferred (not this tip): E-SCAN1, E-UX2, E-QA3 Hypothesis, E-RUN3/4 — backlog only.

---

## 6. Explicit refuse

- DI containers / Guice-style service locator  
- `utils/` grab-bag  
- Service mesh, Backstage-required IDP, Spec Kit WorkflowEngine as runtime  
- Raising complexipy or LOC hard caps to “make room”  
- Rewriting all Stage-0 tools in one tip  
- Suite-wide xdist on the oracle cov cell; LLM-judge as fail_under SoT  
- ECS / DOD / neuromorphic rewrites of `doc_engine`  
- Weakening fail_under **98.7** or policy **16-A**

---

## Invariants (all E-MOD tips)

fail_under **98.7** · complexipy **≤5** · LOC **≤225** (new + split files) · no `utils/` ·
policy **16-A** · SDD one tip · Spec → Implement → Verify → Archive · descriptive names
(no `m`/`o`/`c`).

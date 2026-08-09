---
title: Quality backlog — ordered SDD next actions
status: ACTIVE — one stream at a time
date: 2026-08-08
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
rule: Spec → Implement → Verify → Archive; no parallel SoT thrash
---

# Quality backlog (ordered)

Process for each item: **Spec** (point at decision bullets) → **Implement** (single
stream) → **Verify** (deterministic gates) → **Archive** (CONTRIBUTING / claims as needed).

**Hard invariants:** do not weaken `fail_under=98.7`, complexipy ≤5, or size ≤225.
**Dual-mode code** only after human approve of synthesis decisions **1–31** (min subset
**13–17, 19–21, 25–26, 29**).

---

## P0 — Unblock size / facade debt (LOC-first)

Do these **before** dual-mode if size ratchet fails on touched modules.

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P0.1 | Thin `cli.py` / coverage parsers toward ≤225 (existing `_add_coverage_cli_parsers` or sibling — **no utils bag**) | Embody decision **10** | size-ratchet; complexipy ≤5 |
| P0.2 | Any new measure module starts ≤225 LOC; prefer vertical `doc_engine.ci.coverage_*` slices | Embody DDD / vertical slicing | size + tach |

---

## P1 — Design approval (no code)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P1.1 | Human approve synthesis decisions **1–31** (or explicit subset) | Strategic | Record choice in design memo status |
| P1.2 | Record climb artifact policy **16**: **(A)** distinct XML path **or** **(B)** refuse writing `coverage.xml` | Adopt | Written product choice — closes `[Unknown]` |
| P1.3 | Update `docs/design/coverage-measure-modes-design-2026-08-08.md` status to approved + point at synthesis | Archive | Link check |

---

## P2 — Dual-mode implement (only after P1)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P2.1 | `MeasureMode.ORACLE \| CLIMB` strategies / hexagonal ports; shared wipe + PathCohesion | Adopt **13**, **18** | unit tests; complexipy ≤5; no if/elif god |
| P2.2 | Climb: scoped `--cov`, **no** whole-repo fail_under; stderr banner **11** | Adopt **2–3**, **11**, **17** | tests assert refuse floor claim |
| P2.3 | Implement artifact policy from P1.2 | Adopt **16** | gap-average still reads oracle XML only |
| P2.4 | Naming bar: `scope_package`, `fail_under_floor`, … — no `m`/`o`/`c` | Adopt **14**, **24** | review |
| P2.5 | CONTRIBUTING table: Oracle vs Climb vs Gap vs diff-cover + saliency cadence | Adopt **5**, **26** | claims paths resolve |

---

## P3 — Process / agent hygiene (can parallel *docs only* with P1)

| # | Action | Stance | Verify |
| --- | --- | --- | --- |
| P3.1 | Agent prompts / steering: climb ≠ floor; remesure oracle only on salient triggers | Adopt **17**, **26** | prompt/docs review |
| P3.2 | Encode SDD one-stream in wave1 PR template / CONTRIBUTING note | Adopt **21** | human process |
| P3.3 | Explicit refuse: ungated CONSTRAINTS/baseline rewrite; LLM-judge as fail_under | Refuse **19**, **20** | claims / review |

---

## P4 — Optional later (not prerequisites)

| # | Action | Stance | Notes |
| --- | --- | --- | --- |
| P4.1 | Climb targeting hysteresis (dead-band file re-pick) | Adopt **27** | Advisory only |
| P4.2 | xdist on climb | Refuse v1 / defer **8** | After modes stable |
| P4.3 | Carbon-aware CI scheduling | Optional **23**, **31** | Never block oracle work |
| P4.4 | Profiled Rust helper (not default) | Refuse unless profiled **22** | Cross-link Rust memo |
| P4.5 | Simple CI/agent remesure rate caps | Adopt if storms persist **28** | Before any PID |

---

## Explicit Refuse (do not schedule)

- Scoped Cover% or LLM-judge as 98.7 proof  
- PID / fuzzy “confidence of green” on oracle floor  
- SoA / DOD / ECS / neuromorphic runtime rewrites of `doc_engine`  
- Service mesh, Backstage-required IDP, Argo/Flux product deps  
- Spec Kit WorkflowEngine as mandatory runtime  
- Cross-worktree `coverage combine`  
- Cov cells on every Python version  
- Parallel tip thrash on SoT files  

---

## Suggested next single stream

**Now:** P1.1–P1.3 (approve + artifact policy + memo status).  
**Then:** P0 if size fails on the impl branch.  
**Then:** P2.1–P2.5 dual-mode.  
**Never:** dual-mode + LOC campaign + taxonomy docs rewrite in one tip.

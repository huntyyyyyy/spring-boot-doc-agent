---
category: CI / GitHub Actions / workflow modularity
status: APPROVED — SPEC GATE E-CI0 (2026-08-09)
date: '2026-08-09'
approved_decisions: C1-C6
artifact_policy: C-A
claim_tiers: Evidenced / Confirmed / Unknown
research: docs/research/ci/07-ci-workflow-modularity.md
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
title: 'Design memo: CI workflow modularity'
related: []
last_reviewed: '2026-08-10'
---

# Design memo: CI workflow modularity

> **APPROVED — SPEC GATE E-CI0 (2026-08-09)**
>
> Principal / implementer chat recorded **Approve** of decisions **C1–C6**
> with policy **C-A** (`ci.yml` orchestration-only). Implement epic **E-CI1**
> is unblocked. Does not reopen E-TEST / E-CM / policy **16-A** / Spec Kit
> refuse list.

**Spec record**

| Field | Value |
| --- | --- |
| Decisions | **C1–C6** Approved |
| Policy **C** | **C-A** — thin caller + reusable workflows by BC |
| Research | [`docs/research/ci/07-ci-workflow-modularity.md`](../research/07-ci-workflow-modularity.md) |
| Backlog | [`docs/research/quality-backlog.md`](../research/quality-backlog.md) |

---

## 1. Problem

ABI extraction proved job-level reuse works, but left a **god-sized `test`
job** and **no workflow LOC SoT**. Maintenance cost of GA YAML is evidenced
(arXiv 2409.02366); duplication/smell literature (Gallaba; SCAM 2024) matches
inline heredocs and copy-paste install blocks. `[Evidenced]` / `[Confirmed]`

---

## 2. Policy **C** — locked **C-A**

| Option | Meaning |
| --- | --- |
| **C-A** (locked) | `ci.yml` = triggers/env/concurrency + `uses:` callers only (≤**200** LOC). Logic in reusable workflows + composites + `scripts/ci`. |
| **C-B** | Keep fat `ci.yml`, trim comments only — **Rejected** |
| **C-C** | External org workflow-farm repo — **Rejected** (single-product refuse) |

---

## 3. Decisions (**C1–C6**) — Approved

1. **C1.** CI BCs as reusable workflows: `abi-tests` (exists), `python-gates`,
   `codeql-signals`, `quality-gates`, `sonar` (soft).
2. **C2.** Policy **C-A**: `ci.yml` ≤**200** LOC orchestration-only.
3. **C3.** No inline `python <<'PY'` heredocs in workflows; pin-verify and
   coverage-summary are scripts (optionally wrapped by composites).
4. **C4.** Workflow LOC SoT in `check_workflow_yaml`: advisory if any
   workflow **>225** lines; **hard fail** if `ci.yml` **>200** or any
   workflow **>300**.
5. **C5.** Composites stay in-repo under `.github/actions/` (no CI farm).
6. **C6.** SDD one-stream; do not reopen E-TEST/E-CM.

---

## 4. Adversarial checklist

- [x] Does any extracted job still write `coverage.xml` besides the 3.11 oracle cell?
- [x] Are artifact `needs:` edges preserved (coverage-xml → quality-gates / sonar)?
- [x] Are CodeQL pin env vars still visible to the codeql reusable workflow?
- [x] Does LOC ratchet fail closed on a fat `ci.yml` revival?
- [x] Is Spec Kit / external workflow farm accidentally introduced?

---

## 5. Epic E-CI0 — Spec gate — **DONE**

| ID | Ticket | Acceptance |
| --- | --- | --- |
| CI0-1 | Record Approve **C1–C6** + **C-A** | **Done** — this memo |
| CI0-2 | Research memo 07 | **Done** |

**Exit E-CI0:** Complete. Next stream = **E-CI1**.

---

## 6. Epic E-CI1 — Extract + ratchet (unblocked)

| ID | Ticket | Acceptance |
| --- | --- | --- |
| CI1-1 | `verify_tool_pins.py` + `coverage_run_summary.py` | no `<<'PY'` in workflows |
| CI1-2 | Reusable `python-gates` / `codeql-signals` / `quality-gates` (+ thin sonar) | callers in `ci.yml` |
| CI1-3 | Slim `ci.yml` ≤200 | line count gate |
| CI1-4 | LOC predicates in `check_workflow_yaml` | hard fail per **C4** |
| CI1-5 | CONTRIBUTING layering note | paths resolve |

**Exit E-CI1:** Orchestration-only caller + LOC SoT green.

---

## 7. Approval record

```text
E-CI0 Spec: Approve C1–C6 with policy C-A.
Recorded: 2026-08-09 (principal / implementer chat — plan implement).
```

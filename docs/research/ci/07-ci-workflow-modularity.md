---
title: CI workflow modularity — why YAML god-files form
status: APPROVED — feeds E-CI1 Implement (E-CI0 Spec locked 2026-08-09)
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
synthesis: docs/research/se-quality-synthesis-2026-08-08.md
related: []
last_reviewed: '2026-08-10'
---

# 07 — CI workflow modularity (GHA god-files)

Sibling to **01–06**. Those embodied DDD / dual-mode / test BCs for product
and suite topology. This segment asks the same question for **GitHub Actions
YAML**: why `ci.yml` stays long after ABI extraction, and what to
Embody/Adopt/Refuse before more ad-hoc cuts.

---

## 1. Frame

**Symptom:** After extracting ABI shards to `abi-tests.yml`, `ci.yml` remains
~559 lines. ~57% is the monolithic `test` job (inline pin-verify heredocs,
coverage-summary heredoc, Stage-0/mutate/llms steps, dense `#` essays).
`[Confirmed]` worktree inventory 2026-08-09.

**Category error to refuse:** Spec Kit WorkflowEngine as CI runtime, or an
org-wide “workflow farm” repo for a single-product CLI. Already refused in
synthesis / quality-backlog. `[Confirmed]`

**Real design question:** partition CI into **bounded contexts** (job-level
reusable workflows + step-level composites + scripts) and add a **boolean
workflow LOC SoT** — same shape as E-TEST markers + size ratchet.

---

## 2. Confirmed inventory (this repo)

| Fact | Value | Tier |
| --- | --- | --- |
| `ci.yml` LOC | ~559 (~28% comments) | `[Confirmed]` |
| Dominant job | `test` ~317 lines | `[Confirmed]` |
| Already extracted | `abi-tests.yml`, `setup-python-repo`, `setup-codeql` | `[Confirmed]` |
| `check_workflow_yaml` | parse + security; **no** LOC gate | `[Confirmed]` |
| Inline `<<'PY'` | pin-verify ×2 + coverage summary | `[Confirmed]` |

---

## 3. Primary sources

| Source | Claim | Tier |
| --- | --- | --- |
| arXiv [2409.02366](https://arxiv.org/abs/2409.02366) | GA workflow maintenance is a real cost (bugfix, CI improvement) | `[Evidenced]` |
| Gallaba & McIntosh (TSE; Travis HANSEL) | CI *spec* anti-patterns / duplication are detectable and removable | `[Evidenced]` |
| Khatami et al. SCAM 2024 | GHA workflow smells; frequent change patterns signal debt | `[Evidenced]` |
| GASH (VEM 2024) | Maintenance smells include duplication / hard-to-manage blocks | `[Evidenced]` secondary |
| [GitHub: Reuse workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows) | Reusable workflows = jobs; composites = steps inside one job | `[Evidenced]` |
| DeepWiki snowballr-ci / salesforcecli/github-workflows | Layer workflows + composites by concern (cartography) | `[Evidenced]` cartography |

---

## 4. Embody / Adopt / Refuse

| Item | Stance |
| --- | --- |
| Job-level reusable workflows by CI BC | **Embody** |
| Step composites for install / pin-verify | **Embody** |
| Gate logic only in `scripts/ci` / `doc-engine` | **Embody** |
| Essays → design/CONTRIBUTING, not YAML | **Adopt** |
| Workflow LOC ratchet (boolean SoT) | **Adopt** |
| `ci.yml` orchestration-only (policy **C-A**) | **Adopt** |
| Spec Kit WorkflowEngine / external CI farm | **Refuse** |
| Delete rationale without archive | **Refuse** |
| Cov combine / suite-wide xdist | **Refuse** |

---

## 5. Link forward

Design Spec: `docs/design/ci-workflow-modularity-design-2026-08-09.md`  
Backlog: E-CI0 → E-CI1.

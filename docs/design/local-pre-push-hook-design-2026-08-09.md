---
category: Local pre-push git hook / first-line quality
status: APPROVED — SPEC GATE E-HOOK0 (2026-08-09) — merge Approve of HOOK1–HOOK12 (modern-landscape amendment)
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/27-local-pre-push-hook-2026.md
  - scripts/ci/pre_pr.py
  - .githooks/pre-push
  - docs/design/quality-policy-setpoints-design-2026-08-09.md
do_not:
  - make Sonar fail_under / merge SoT
  - require remote Actions to discover complexipy/size/jscpd/tach failures
  - grow pre_pr into a god file — extract suite helpers
spec_gate: APPROVED E-HOOK0 (2026-08-09) — HOOK1–HOOK12
---

# Design memo: local pre-push as first-line quality

> **APPROVED — SPEC GATE E-HOOK0 (2026-08-09)**

## 1. Problem

`.githooks/pre-push` exists but is easy to miss (opt-in hooksPath; Cursor
override). `pre_pr --auto` also skips in-repo `quality-gates`, so tip writers
can push green local pytest and still learn complexipy/size/dup failures only
on remote. Force-push does **not** skip `pre-push` unless `--no-verify`.

## 2. Verdict

| Question | Answer |
| --- | --- |
| When does local quality run? | Every `git push` / force-push via `pre-push` → `pre_pr` |
| Modern hook managers? | **Embody** `.githooks`; **Refuse** husky primary; **Defer** lefthook (&lt;10k★); **Spike** pre-commit wrapper |
| Local Actions replay (`act`)? | **Spike** for workflow debug — **not** default every-push SoT |
| Remote CI role? | Merge-time **second line**, not first discovery |
| Sonar local? | Opt-in **advisory** (Docker Community + scanner); never SoT |
| Cognitive/size SoT locally? | `doc-engine quality-gates --skip-coverage` on standard/full |

Research amendment: [`process/27`](../research/process/27-local-pre-push-hook-2026.md) §0–§5 (modern landscape + ★ table).

## 3. Locked decisions (HOOK1–HOOK12)

| ID | Decision |
| --- | --- |
| HOOK1 | `.githooks/pre-push` remains the committed SoT entry; force-push still invokes it |
| HOOK2 | `scripts/ci/install_git_hooks.py` enables hooksPath **or** installs a chain `pre-push` into an external hooks dir (Cursor) |
| HOOK3 | Prefer `.venv/bin/python` when present inside the hook |
| HOOK4 | `PRE_PR_MODE=full` env overrides `--auto` for tip writers wanting Stage-0 locally |
| HOOK5 | standard/full/actions_outage include hard `in_repo_quality_gates` with `--skip-coverage` (compare-ref from `PRE_PR_COMPARE_REF` or `origin/main`) |
| HOOK6 | Cover% oracle remesure stays CI 3.11 / explicit local remesure — push path does not pretend oracle without XML |
| HOOK7 | Local SonarQube: compose + advisory scanner when `SONAR_HOST_URL` + `SONAR_TOKEN` set; else no-op advisory |
| HOOK8 | **Refuse** Sonar as boolean / fail_under SoT (STACK / constitution) |
| HOOK9 | Bypass remains logged `PRE_PR_SKIP` + reason; tip practice refuses `--no-verify` except emergency |
| HOOK10 | After E-HOOK1 Done, Active tip returns to **E-COH1** |
| HOOK11 | **Spike (Defer):** `pre-commit` framework as thin installer that only runs `pre_pr` — no second suite catalog |
| HOOK12 | **Spike (Defer):** documented `nektos/act` recipe for workflow YAML debug / outage-adjacent; refuse act-on-every-push |

## 4. CGQ3 Accept (E-HOOK1)

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| Hook never installed | HOOK2 | process/27 §3–5 | `install_git_hooks --check` green; chain file when hooksPath external |
| Quality only on remote | HOOK5 | quality-gates / KNOB owners | `build_suites` includes `in_repo_quality_gates` |
| Sonar confusion | HOOK7–8 | STACK / CONTRIBUTING Sonar soft | advisory-only; docs say not SoT |
| Framework FOMO without ★ bar | HOOK11–12 + process/27 §2 | STACK ≥10k; ★ table | husky Refuse; lefthook Defer; act Spike only |

## 5. Out of scope (until Spike ask)

- Migrating tip SoT to husky / lefthook / full pre-commit hook zoo
- Making Cover% oracle part of every push
- Blocking `--no-verify` at the git binary (impossible without wrapper)
- Adopting &lt;10k★ local-GHA runners (gitgate / wsr / local-ci / actrun)

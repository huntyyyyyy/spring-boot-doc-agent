---
title: Local pre-push gate as first-line quality (no remote required)
status: APPROVED — SPEC GATE E-HOOK0 (2026-08-09) — amended modern-landscape pass
date: '2026-08-09'
epic: E-HOOK0
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/design/local-pre-push-hook-design-2026-08-09.md
- docs/research/process/22-stack-rescope-10k-star-bar-2026.md
- docs/research/quality-backlog.md
- scripts/ci/pre_pr.py
- .githooks/pre-push
do_not:
- treat SonarCloud/SonarQube as fail_under / merge SoT
- rely on remote Actions as the first discovery of local quality debt
- Adopt ★-wash (&lt;10k) local-GHA runners as tip SoT
- replace pre_pr suite SoT with “run all of ci.yml via act on every push”
last_reviewed: '2026-08-10'
---

# Process research: local pre-push hook (E-HOOK0)

## 0. Honesty note (amendment)

The first draft of this memo **deferred** husky/lefthook/pre-commit as a
bundle without a ★-dated landscape. That was insufficient for
principal-SE / STACK. This amendment records modern approaches with
**Evidenced** primary surfaces + **Confirmed** tip constraints, then
locks Embody/Adopt/Refuse.

## 1. Question

How do tip writers get **local** fail-closed quality feedback on every
`git push` (including `--force` / `--force-with-lease`) without burning remote
CI minutes — and which **modern** hook / local-Actions / Sonar options fit
this Python CLI under the ≥10k★ bar?

## 2. Modern landscape (2026-08-09)

### 2.1 Git hook managers

| Tool | Stars (gh API) | Last push | Fit for this repo | Stance |
| --- | ---: | --- | --- | --- |
| **typicode/husky** | 35 253 | 2026-03-19 | Node `prepare` / npm-centric; our `package.json` is jscpd-only | **Refuse** as primary installer (wrong stack) |
| **pre-commit/pre-commit** | 15 496 | 2026-07-21 | Python-native framework; large hook ecosystem; ≥10k★ | **Adopt** as *optional* meta-installer Spike — must only call `pre_pr`, not fork suite SoT |
| **evilmartians/lefthook** | 8 625 | 2026-08-03 | Fast Go binary, parallel, polyglot — modern favorite in 2026 blogs | **Defer** under STACK (&lt;10k★); revisit if crosses bar / human override |
| Native `core.hooksPath` + committed `.githooks/` | n/a (git) | — | Already Confirmed in tip; zero new runtime | **Embody** |

Industry pattern (Evidenced — 2026 hook comparison writeups): keep
**pre-commit/pre-push fast enough not to train `--no-verify`**; mirror the
same checks in CI as second line. Force-push still runs `pre-push` unless
`--no-verify` (Evidenced — git hooks semantics).

### 2.2 Local GitHub Actions runners (“don’t use remote to find red”)

| Tool | Stars | Notes | Stance |
| --- | ---: | --- | --- |
| **nektos/act** | 71 426 | Mature local GHA runner; Docker-heavy; imperfect matrix/parity | **Adopt Spike** — optional workflow debug / outage-adjacent; **not** default every-push path |
| redwoodjs/local-ci | 747 | Official runner + local API emulation — interesting, young | **Refuse** Adopt (★-wash); watch |
| plsft/gitgate, rehearse, ectorial/wsr, mizchi/actrun | 0–662 | 2026 “faster than act” wave | **Refuse** Adopt (★-wash / alpha) |

**Category error to avoid:** “run the YAML” ≠ “own the quality SoT.” This
repo’s SoT is already **concept suites** in `pre_pr` / `quality-gates`, not
workflow YAML fidelity. Full `act` on every push would burn local Docker
time, still miss oracle Cover% nuances, and duplicate `pre_pr`.

### 2.3 Local SonarQube

| Claim | Tier | Stance |
| --- | --- | --- |
| Community Docker + `sonar-scanner-cli` is the supported local analysis path | Evidenced — SonarSource scanner docs 2026 | **Adopt** advisory |
| SonarCloud Free QG cannot encode 98.7 / complexipy ≤5 | Confirmed — CONTRIBUTING | **Refuse** as SoT |
| In-repo cognitive SoT remains complexipy | Confirmed — constitution / KNOB | Keep |

## 3. Tip constraints (Confirmed)

| Constraint | Implication |
| --- | --- |
| Cursor Cloud overrides `core.hooksPath` to agent-hooks | Need **install or chain**, not only `git config` docs |
| `pre_pr` already mirrors hard suites; was missing `quality-gates` | Wire local gates into standard/full |
| STACK ≥10k★ for new Adopt | lefthook / local-ci / gitgate not Adopt yet |
| No `utils/` / god `quality_knobs` | Hook installer stays tiny; suites stay concept-owned |

## 4. Alternatives → verdict

| Option | Stance |
| --- | --- |
| Remote CI as first quality discovery | **Refuse** |
| Husky as primary | **Refuse** (Node theater) |
| Lefthook as primary | **Defer** (&lt;10k★) |
| pre-commit framework replacing `.githooks` | **Spike** — only if it installs/calls `pre_pr`; no second suite catalog |
| `act`/local-ci on every push | **Refuse** as default; **Spike** act for workflow debug |
| Alpha “faster than act” runners | **Refuse** Adopt |
| `.githooks/pre-push` → `pre_pr` + `install_git_hooks` chain + local `quality-gates` | **Embody** |
| Local Sonar advisory | **Adopt** |
| Sonar as fail_under | **Refuse** |

## 5. One-page verdict

**Embody** committed `.githooks` + install/chain (Cursor-safe) calling
`pre_pr`. **Adopt** in-repo `quality-gates --skip-coverage` on the push path
so complexity/size/dup/tach fail locally without remote. **Adopt** optional
Sonar Community advisory. **Spike** (not tip-blocking): (a) pre-commit
wrapper that only invokes `pre_pr`; (b) documented `act` recipe for workflow
YAML debug. **Refuse** husky primary, ★-wash local runners, Sonar-as-SoT,
and “full Actions replay on every push.”

Remote CI remains merge-time **second line**.

## 6. Spec gate

Design memo **HOOK1–HOOK12** (HOOK11–12 = Spikes). Implement **E-HOOK1**
green slice; Spikes only on human ask. Then return tip to **E-COH1**.

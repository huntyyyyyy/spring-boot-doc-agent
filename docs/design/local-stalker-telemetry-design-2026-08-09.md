---
category: Local stalker telemetry ETL / masked suite failures
status: APPROVED — SPEC GATE E-TEL0 (2026-08-09) — TEL1–TEL10
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/28-local-stalker-telemetry-etl-2026.md
- docs/design/local-pre-push-hook-design-2026-08-09.md
- docs/design/suite-stalking-sensors-design-2026-08-09.md
do_not:
- put suite logs under docs/research/
- weaken advisory→hard for intentional survivor reporting without Spec
- treat telemetry as oracle Cover%
spec_gate: APPROVED E-TEL0 (2026-08-09) — TEL1–TEL10
title: 'Design memo: local stalker telemetry ETL'
last_reviewed: '2026-08-10'
---

# Design memo: local stalker telemetry ETL

> **APPROVED — SPEC GATE E-TEL0 (2026-08-09)**

## 1. Problem

`pre_pr` can overall=pass while an advisory suite exits non-zero (e.g.
`mutation_driver` import crash). Remote CI runs the same command as a named
step without `continue-on-error`, so remote fails and local looked green.
Receipts store `exit=N` only — no log body for agents to debug.

## 2. Verdict

| Question | Answer |
| --- | --- |
| Fix mutation_driver? | Yes — `-m` entry + robust import; CI + pre_pr aligned |
| Local severity? | Tool crash / non-zero driver → **hard** on full path |
| Telemetry home? | `.git/pre-pr-telemetry/<sha>-<mode>/` (gitignored area under `.git`) |
| Stalker role? | G7 reads last index: advisory≠0 → finding (fail-closed in scan when wired hard? advisory finding in pre_pr stalker) |

## 3. ETL shape

| Stage | Module | Artifact |
| --- | --- | --- |
| Extract | tee during `_suite` | `suites/<name>.log` (stdout+stderr) |
| Transform | index writer | `index.json` — name, kind, status, exit, duration_ms, log path, error_excerpt |
| Load | CLI + G7 | `stalker_telemetry show`; `scan_masked_advisory` finding |

## 4. Locked decisions (TEL1–TEL10)

| ID | Decision |
| --- | --- |
| TEL1 | Fix `mutation_driver` to run as `python -m tests.spring_signals.mutation_driver` (CI + pre_pr) |
| TEL2 | Prefer same-package import inside driver (no bare `tests.` dependency on script path) |
| TEL3 | `mutation_driver` suite is **hard** on `--full` / outage (survivors still ENFORCE=False → exit 0) |
| TEL4 | Every pre_pr suite tees logs into `.git/pre-pr-telemetry/…` |
| TEL5 | `index.json` is the transform SoR for one run; receipt gains `telemetry_dir` |
| TEL6 | G7 `masked_advisory_nonzero`: last index advisory with exit≠0 |
| TEL7 | CLI `scripts/ci/stalker_telemetry.py show` prints fails + excerpt |
| TEL8 | Telemetry never rewrites fail_under / baselines |
| TEL9 | Findings ledger stays G1–G6 research; G7 may append when ledger on |
| TEL10 | After E-TEL1 Done, Active tip returns to **E-COH1** |

## 5. CGQ3 Accept

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| Local green / remote red import | TEL1–TEL3 | process/28 §1 | `python -m …mutation_driver` exit 0; pre_pr hard suite |
| No local debugger | TEL4–TEL7 | process/28 §4 | index.json + show CLI + G7 |
| SoT pollution | TEL8–TEL9 | STK / constitution | `.git/` only; sensors≠oracle |

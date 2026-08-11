---
category: Local domain pytest selection / fine ABI shards
status: APPROVED — SPEC GATE E-SEL0 (2026-08-09) — SEL1–SEL10
date: '2026-08-09'
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/research/process/29-local-domain-pytest-select-2026.md
- docs/design/test-suite-parallel-domains-design-2026-08-08.md
- scripts/ci/pre_pr.py
do_not:
- xdist on cov oracle cell
- skip oracle via testmon
- silent empty selection (must fail-closed to full suite)
spec_gate: APPROVED E-SEL0 (2026-08-09) — SEL1–SEL10
title: 'Design memo: domain select + fine ABI paths'
last_reviewed: '2026-08-10'
---

# Design memo: domain select + fine ABI paths

> **APPROVED — SPEC GATE E-SEL0 (2026-08-09)**

## 1. Locked decisions (SEL1–SEL10)

| ID | Decision |
| --- | --- |
| SEL1 | Mixed-marker collection dirs emit **per-file** paths in ABI matrix; pure dirs stay dir paths |
| SEL2 | `pre_pr` **standard** builds pytest argv from changed paths → closed prefix→marker map |
| SEL3 | Unknown code path or empty selection → **full** `tests/` (fail-closed) |
| SEL4 | `--full` / `--actions-outage` always full `tests/` |
| SEL5 | Selection uses `paths_for_marker` + `-m <marker expr>`; never invents unmarked runs |
| SEL6 | Local `--junitxml=.git/pre-pr-pytest.junit.xml` + suite_timing summary print (sensor) |
| SEL7 | Receipt / telemetry records `pytest_select` markers or `"full"` |
| SEL8 | **Refuse** pytest-testmon as SoT; **Refuse** xdist on oracle |
| SEL9 | Regression tests: mixed-dir matrix has file paths; ci-only change selects `domain_ci_meta` |
| SEL10 | After E-SEL1 Done, Active tip returns to **E-COH1** |

## 2. CGQ3 Accept

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| Fat ABI collect | SEL1 | T-A; process/29 §2 | climb paths include `.py` files when dir mixed |
| 57s local pytest always | SEL2–SEL5 | E-RUN4 shape; T-A | argv narrow for ci-only; full on unknown |
| False green skip | SEL3 | constitution / E-RUN refuse RTS-oracle | empty/unknown → full |

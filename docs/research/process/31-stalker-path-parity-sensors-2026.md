---
title: E-TEL2 — Path-parity stalker sensors (oracle / CodeQL / suite map)
status: APPROVED — SPEC GATE E-TEL2 (2026-08-09)
date: 2026-08-09
epic: E-TEL2
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/process/28-local-stalker-telemetry-etl-2026.md
  - docs/research/process/19-watch-stalker-agents-context-lean-2026.md
  - docs/research/ci/17-codeql-signals-skip-fingerprint-2026.md
  - docs/research/process/30-local-oracle-push-parity-2026.md
do_not:
  - LLM-as-judge / Bloom Evaluate as merge SoT
  - OTel/APM as tip SoT
  - sensors rewriting fail_under
---

# Process research: principal-SE path-parity sensors

## 1. Problem

G1–G7 catch tip hygiene and masked advisory *after* the fact. They do not sense
**local plant ≠ remote plant** (oracle skip), **CodeQL fingerprint absence**,
or **workflow↔suite severity skew**. Principal diagnosis needs decidable
predicates + witnesses across Remember→Analyze (Bloom) without Create-via-LLM.

## 2. Verdict

**Adopt** package `stalker_path_parity` with G8–G10:

| ID | Sensor | Witness |
| --- | --- | --- |
| G8 | `oracle_cell_posture` | pre_pr / quality-gates skip-coverage vs python-gates fail_under |
| G9 | `codeql_change_presence` | `codeql_signals_change_gate.py` + workflow `if:` seam |
| G10 | `workflow_suite_map` | remote-hard suite missing or advisory-only locally |

Sensors remain advisory in `stalker_scan` (actuator = Spec/Implement). Refuse
LLM Evaluate as SoT. Mental models: control loop, SoR vs derived, fail-closed.

## 3. CGQ3 Accept

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| plant asymmetry | fitness-function sensors | process/24 §2.1 | `tests/ci/test_stalker_path_parity.py` |
| CodeQL waste invisible | fingerprint presence (E-CQL1) | §2.1 | G9 fails closed when gate script absent |

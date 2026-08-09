---
title: E-HOOK2 — Local oracle Cover% on push (parity with remote 3.11)
status: APPROVED — SPEC GATE E-HOOK2 (2026-08-09)
date: 2026-08-09
epic: E-HOOK2
claim_tiers: Evidenced / Confirmed / Unknown
related:
  - docs/design/local-pre-push-hook-design-2026-08-09.md
  - docs/research/process/27-local-pre-push-hook-2026.md
  - docs/research/ci/17-codeql-signals-skip-fingerprint-2026.md
do_not:
  - treat domain-select pytest as 98.7 proof
  - climb XML as oracle SoR
  - weaken DEFAULT_FLOOR below 98.7
---

# Process research: local oracle must bite before remote spend

## 1. Problem (Confirmed)

`pre_pr` / pre-push can be overall=pass while remote CI fails `--cov-fail-under=98.7`
because HOOK6 deliberately skipped oracle remesure and quality-gates used
`--skip-coverage`. Local green ≠ remote Cover% predicate.

## 2. Verdict

**Amend HOOK6.** On `standard`/`full`/`actions_outage` when package or test trees
changed (or always on `--full`), replace bare pytest with
`doc-engine coverage-measure` (oracle → `coverage.xml` + fail_under 98.7). Then
run quality-gates **with** coverage XML (diff-cover). Keep `--fast` and
`PRE_PR_SKIP_ORACLE=1` escape. Domain select remains for non-oracle loops only.

## 3. CGQ3 Accept

| Concern | Remedy | Depth | Witness |
| --- | --- | --- | --- |
| local plant ≠ remote Cover% plant | single-write oracle remesure (SOL dual-write refuse) | process/24 §2.1 | `oracle_coverage` hard in pre_pr; tests assert argv has fail_under |
| remote resource waste | fail-closed before push | fitness | pre_pr receipt shows oracle suite when src/tests change |

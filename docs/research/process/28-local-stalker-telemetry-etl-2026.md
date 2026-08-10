---
title: Local stalker telemetry ETL — suite logs + masked-failure sensor
status: APPROVED — SPEC GATE E-TEL0 (2026-08-09)
date: '2026-08-09'
epic: E-TEL0
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/design/local-stalker-telemetry-design-2026-08-09.md
- docs/research/process/19-watch-stalker-agents-context-lean-2026.md
- docs/design/suite-stalking-sensors-design-2026-08-09.md
do_not:
- treat telemetry ETL as Cover% / fail_under SoT
- dump suite logs into docs/research/findings (keep .git/ local)
- leave advisory suites that crash on import as local-green / remote-red
last_reviewed: '2026-08-10'
---

# Process research: local stalker telemetry ETL (E-TEL0)

## 1. Incident (Confirmed)

Remote CI (`python-gates.yml`): `python3 tests/spring_signals/mutation_driver.py`
→ `ModuleNotFoundError: No module named 'tests'`.

Local `pre_pr --full` ran the same script as **advisory**, recorded `exit=1`,
and still overall=pass — so tip writers/agents did not fail-closed before push.

Root cause: script path puts `tests/spring_signals/` on `sys.path[0]`, not repo
root; `from tests.spring_signals…` needs root (or `-m` / same-dir import).

## 2. Question

How does local stalker **extract → transform → load** suite metrics/logs so
developers and agents debug locally, and how do we stop masked advisory
crashes from diverging from remote?

## 3. Modern / prior art (brief)

| Pattern | Tier | Note |
| --- | --- | --- |
| pre_pr receipt JSON (exit only) | Confirmed | No stdout capture today |
| suite_timing junit ETL (E-RUN) | Confirmed | CI 3.11 cell; not local pre_pr |
| Stalker G1–G6 ledger | Confirmed | Sensors; `--no-ledger` in pre_pr |
| OTel / full APM | Evidenced refuse for tip | E-RUN D12 deferred; too heavy |

## 4. Verdict

**Embody** fix `mutation_driver` invocation (`-m` + import hygiene) and treat
tool crashes as **hard** on local full path. **Adopt** local telemetry store
under `.git/pre-pr-telemetry/` (E: suite tee logs · T: index.json · L: CLI +
G7 sensor for advisory≠0). **Refuse** shipping logs into research findings;
**Refuse** OTel as tip SoT.

## 5. Spec

Design **TEL1–TEL10**; Implement **E-TEL1** with the mutation_driver fix in the
same stream.

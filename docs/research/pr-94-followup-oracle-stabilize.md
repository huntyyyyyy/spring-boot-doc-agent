# Follow-up after PR #94 merge (oracle stabilize)

Inherited debt from merging #94 while **UNSTABLE**:

- Run: https://github.com/huntyyyyyy/spring-boot-doc-agent/actions/runs/31297580936
- Red: `Python gates / test (3.11)` — `93 failed, 1664 passed, 61 errors`
- Dominant signal: `TypeError: …setUpClass() missing 1 required positional argument: 'cls'`
  on spring_drift unittest classes (and cascading ERROR collection).

## Invariants (do not reopen)

- Single-writer Cover% oracle: only `coverage.xml` from one 3.11 `pytest tests/` cell
  (policy **16-A** / **T9** / **T14**).
- No shard+`coverage combine` for `fail_under`; no suite-wide xdist without E-TEST2 Spec.

## Goal of this branch

Reproduce → minimal fix for the 3.11 oracle failures → green `python-gates` 3.11
without weakening the floor.

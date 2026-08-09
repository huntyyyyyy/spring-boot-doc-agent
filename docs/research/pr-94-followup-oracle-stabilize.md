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

## E-OR1 Spec (ruff ownership / oracle unblock)

**Confirmed:** tip CI failed at `ruff check` (F401 false facade re-exports). Pytest
never ran, so `coverage.xml` was absent and the always-on gap-average step reported
`coverage.xml missing` as a downstream symptom — not an oracle SoT failure.

**Spec gate:**

1. Measurement helpers live only in `doc_engine.ci.size_measure`
   (`line_count`, `statement_count`, `_visit_functions`).
2. Cobertura condition parsing lives only in `doc_engine.ci.coverage_report`
   (`_parse_condition_coverage`).
3. `coverage_gap_average` / `size_ratchet` import from those modules **only what
   they call** (no test-only re-export wallpaper; no `# noqa: F401`).
4. Edge tests assert against the **owner** module, not a facade alias.
5. Invariants unchanged: fail_under **98.7**, LOC ≤225, complexipy ≤5, 16-A
   single-writer `coverage.xml`.

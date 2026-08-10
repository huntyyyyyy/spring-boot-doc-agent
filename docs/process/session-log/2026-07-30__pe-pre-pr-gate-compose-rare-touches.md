# Session log — 2026-07-30

Lead: **PE pre-PR gate (compose + rare touches)**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 5. Newest at the bottom of this file.

---

## 2026-07-30 ? PE pre-PR gate (compose + rare touches)



Commit: 065680a



Tests: 24 targeted (pre_pr + workflow ramp + verify_certification); pre_pr --fast pass; --auto standard pytest pass



Assumptions affected:



- Local fail-closed before PR ? [New info ? `scripts/ci/pre_pr.py` + `.githooks/pre-push`; CI still merge second line]



- Workflow security while Actions stay tag-pinned ? [New info ? severity ramp in `check_workflow_yaml.py`; medium `actions/*@vN` advisory only]



- `test_verify_certification` pre-slice dict fixtures ? [Resolved ? reuse `build_certification_report` / `write_certification_json`; incomplete dict fails schema gate]



Phase 2 backlog (pick one scanner stack after SHA-pin):



- SHA-pin all `uses:` (`uses: ?@sha # vX.Y.Z`); then johnbillion (actionlint + zizmor SARIF ? poutine/octoscan) or i9wa4 (actionlint + ghalint + pinact --check + zizmor)



- ghalint: `persist-credentials: false`, `timeout-minutes`



- Harden-Runner `egress-policy: audit` first; gitleaks with baseline; delta mutation annotations (mutate stays advisory until watched); Meta ACH = research only



Files touched: scripts/ci/pre_pr.py, scripts/ci/check_workflow_yaml.py, .githooks/pre-push, .github/workflows/ci.yml, tests/test_pre_pr.py, tests/test_check_workflow_yaml.py, tests/test_verify_certification.py, scripts/README.md, CONTRIBUTING.md, claude/session-log.md







## 2026-07-30 ? tests/ subdirectory layout (mirror scripts/)



Commit: 065680a



Tests: 150 passed (suite_layout + pre_pr + require_hardened + check_repo_claims); suite_layout discovers 51 nested suites; pre_pr --fast pass



Assumptions affected:



- Flat `tests/test_*.py` inventory / `suite_layout.glob` ? [Resolved ? taxonomy `tests/{ci,ratchets,coverage,doc_engine,adapters}/`; `suite_paths`/`suite_file_for_module` use `rglob`]



- `verify:` / current-state docs citing flat suite paths ? [Resolved ? nested paths; `tests/` added to `OWN_PATH_PREFIXES`]



Files touched: tests/** (layout + README), scripts/ci/suite_layout.py, scripts/ci/check_repo_claims.py, adapters/claude/hooks/require_hardened_tests.py, CONSTRAINTS.md, STATUS.md, MATURITY_ASSESSMENT.md, README.md, steering verify paths, scripts/README.md, claude/session-log.md







## 2026-07-30 ? certification verify tests vs schema gate



Commit: 065680a



Tests: 36/36 (verify_certification + compliance + certification schema round-trip)



Assumptions affected:



- Hand-rolled `{"certified": True}` fixtures still valid after CertificationReport.model_validate ? [Resolved ? tests mint via build_certification_report/write_certification_json; incomplete dicts assert schema failure]



- Empty gate audit can certify when profile_gate_ids non-empty ? [Resolved ? build_certification_report treats missing required gates as failures]



Files touched: src/doc_engine/pipeline/compliance.py, tests/doc_engine/test_verify_certification.py, tests/doc_engine/test_compliance.py, claude/session-log.md







## 2026-07-30 ? B1 client identifier tracked-tree denylist



Commit: 065680a



Tests: 33 passed (check_no_client_identifiers + materialize isolation); --tracked-tree clean



Assumptions affected:



- Client checkout names only caught on review / oracle aggregate ? [Resolved ? `--tracked-tree` denylist + CI/pre_pr wiring; tokens only in client_identifier_denylist.txt]



- Adoption-blockers B1 open ? [Resolved]



Files touched: scripts/ci/check_no_client_identifiers.py, scripts/ci/client_identifier_denylist.txt, scripts/ci/pre_pr.py, .github/workflows/ci.yml, scripts/coverage/rule_coverage_baseline.json, tests/ci/test_check_no_client_identifiers.py, tests/doc_engine/test_artifact_schemas.py, tests/ratchets/test_mutate.py, claude/session-log.md, claude/research/adoption-blockers-queue-2026-07-30.md







## 2026-07-30 ? B2 live certification chain



Commit: c235950



Tests: 17 passed (test_live_gates + test_verify_certification)



Assumptions affected:



- pipeline gates does not rewrite certification.json ? [Resolved ? always writes generative_executor=live + gate audit]



- certification verify accepts mock/none certified:true ? [Resolved ? reject unless --allow-mock]



- Adoption-blockers B2 open ? [Resolved]



Files touched: src/doc_engine/pipeline/live_gates.py, src/doc_engine/tools/certification.py, src/doc_engine/cli.py, tests/doc_engine/test_live_gates.py, tests/doc_engine/test_verify_certification.py, .github/workflows/doc-engine.yml, action.yml, adapters/github/workflow-snippet.yml, claude/research/adoption-blockers-queue-2026-07-30.md, claude/session-log.md








# scripts/ — meta CI and fixtures (not the product)

Product Stage-0 / pipeline tools live under `src/doc_engine/` and are invoked as
`python -m doc_engine.tools.<mod>` or `doc-engine`. **Do not re-add product CLIs
here** (STATUS dual-home lock).

This tree is repo meta only:

| Directory | Owns |
|-----------|------|
| `ci/` | Gate checkers: `check_repo_claims`, `check_code_quality`, `check_llms_coverage`, `check_workflow_yaml`, `check_no_client_identifiers`, `pre_pr`, `setup_codeql.sh`, plus `suite_layout`, `prompt_contracts` |
| `ratchets/` | Gate-mutator harness (`mutate` + OCP `mutator_registry` / `gate_mutators`), Type-1 `java_perturbations`, `set_delta`, AST signatures, baselines (`*_baseline.json`). Three taxonomies — see CONTRIBUTING.md “Mutation-scope taxonomies”; not PIT. |
| `coverage/` | Rule non-vacuity / backtest: `rule_coverage`, `semgrep_rule_coverage`, fixtures, `spring_semgrep_rules.yml` |
| `schemas/` | JSON Schema exports derived from `doc_engine.pipeline.artifacts` (+ `run_manifest.schema.json`) |
| `fixtures/` | Stage-0 spring_signals fixture tree + snapshot JSON + regenerate/oracle helpers |

## Principal-engineer pre-PR gate

Local fail-closed orchestrator (CI remains merge-time second line). Git cannot
intercept `gh pr create`; push (including force-push) is the choke point via
`.githooks/pre-push`.

```bash
# one-time per clone (sets hooksPath or chains into Cursor agent-hooks)
python3 scripts/ci/install_git_hooks.py
python3 scripts/ci/install_git_hooks.py --check

python3 scripts/ci/pre_pr.py --auto            # default from .githooks/pre-push
python3 scripts/ci/pre_pr.py --fast            # tier 0 + claims
python3 scripts/ci/pre_pr.py --full            # + Stage-0 + advisory mutate/metrics/sonar
python3 scripts/ci/pre_pr.py --actions-outage  # CI parity when Actions is down
PRE_PR_MODE=full git push                      # tip override without editing the hook
```

| Mode | Hard suites |
|------|-------------|
| `--fast` | workflow YAML (+ security severity ramp), tool-doctor, ruff, repo_claims |
| `--auto` / default | docs-only → fast; otherwise **standard** (quality checkers, pytest, **in-repo quality-gates** with `--skip-coverage`) |
| `--full` | all hard + portable Stage-0 + advisory mutate/metrics + optional local Sonar |
| `--actions-outage` | `--full` + CodeQL invariants/compile/QL tests/fixture runtime + `certification verify --allow-mock` (scan_only + certified) |

`in_repo_quality_gates` runs `doc-engine quality-gates --compare-ref … --skip-coverage`
so complexipy / size / jscpd / tach fail **locally** without needing remote CI or a
fresh Cover% oracle XML (oracle remesure stays the 3.11 CI cell / explicit remesure).
Override base with `PRE_PR_COMPARE_REF=origin/main`.

Local SonarQube (advisory): [`scripts/ci/sonar-local/README.md`](ci/sonar-local/README.md).
Modern approach choices (husky / lefthook / pre-commit / act ★ table):
[`docs/research/process/27-local-pre-push-hook-2026.md`](../docs/research/process/27-local-pre-push-hook-2026.md).
Local suite telemetry (ETL under `.git/pre-pr-telemetry/`; debugger CLI):
`python3 scripts/ci/stalker_telemetry.py show --failures-only`
([`process/28`](../docs/research/process/28-local-stalker-telemetry-etl-2026.md)).

Receipt: `.git/pre-pr-receipt.json` (schema 2: optional `attestation` /
`github_status_note` for outage mode). Bypass (logged): `PRE_PR_SKIP=1` **and**
`PRE_PR_SKIP_REASON='…'` (≥8 chars) → `.git/pre-pr-bypass.log`. Bypass is
**refused** under `--actions-outage`. Tip practice refuses `git push --no-verify`.

`check_workflow_yaml.py` hard-fails critical/high Actions footguns (script
injection, write-all, missing permissions, third-party unpinned tags);
`actions/*@vN` stays **advisory** until a SHA-pin PR.

### Actions outage (local CI parity)

When GitHub Actions is down (action download 503s, jobs stuck queued — see
https://www.githubstatus.com Actions component), run hermetic CI parity locally
instead of waiting on the second line:

1. Confirm the outage on GitHub Status (Actions = major/partial outage).
2. Activate the venv. Ensure **Java 17+** and **bash** (Git Bash on Windows).
3. Bootstrap the pinned CodeQL CLI if needed (same digest as `ci.yml`):
   ```bash
   bash scripts/ci/setup_codeql.sh
   eval "$(bash scripts/ci/setup_codeql.sh --print-path-export)"
   ```
   Non-linux64: set `CODEQL_BUNDLE_URL` + `CODEQL_SHA256` from the matching
   codeql-action release asset, or put an existing `codeql` v2.26.2 on `PATH`.
4. Run:
   ```bash
   python3 scripts/ci/pre_pr.py --actions-outage --status-url 'https://www.githubstatus.com/'
   ```
5. On overall pass, keep `.git/pre-pr-receipt.json` (`attestation: actions_outage`)
   with the push/PR; cite `git_sha` in the PR comment.
6. When Actions recovers, re-run CI on the same SHA — the receipt is interim
   attestation, not a permanent substitute for the merge-time second line.

**Non-goals for outage mode:** Pages deploy, Artifactory ocs databases,
`pr-comment`, and anything that would revive `verify_llms_docs.py`.

## Invoke examples

```bash
python3 scripts/ci/check_repo_claims.py
python3 scripts/ci/check_code_quality.py
python3 scripts/ci/pre_pr.py --fast
bash scripts/ci/setup_codeql.sh   # optional; needed for --actions-outage
python3 scripts/coverage/rule_coverage.py
python3 scripts/ratchets/mutate.py
```

Baselines for the CI checkers live in `ratchets/`; coverage baselines stay beside the coverage runners. Path helpers: `doc_engine.paths.scripts_dir()` / `scripts_meta_path_entries()`.

Suites mirror this taxonomy under [`tests/`](../tests/README.md) (`ci/`, `ratchets/`, `coverage/`, `doc_engine/`, `adapters/`). Discovery is recursive via `suite_layout.suite_paths`.

## Local grading pack (Windows / IntelliJ)

Do **not** run `docs/process/local-grading-pack.md` via the Markdown play button.
Use `scripts/ci/run_local_grading_pack.cmd` (Git Bash) or the `.sh` on Linux:

```text
# Git Bash:
./scripts/ci/run_local_grading_pack.sh doctor
# cmd / IntelliJ Batch (not: python ...cmd):
scripts\ci\run_local_grading_pack.cmd doctor
```

Logs: `local-runs/logs/`. Checklist: `docs/process/local-grading-pack.md`.

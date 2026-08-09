# spring-boot-doc-agent

**doc-engine** documents Spring Boot repositories: deterministic Stage 0 scan, optional interview, and a fixed **fourteen-file** markdown set with machine-checkable `certification.json` gates.

The Claude Code plugin under [`adapters/claude/`](adapters/claude/) is an optional adapter for live generative stages. Operators and CI should use the CLI.

```bash
pip install -r requirements.txt
pip install -e .
doc-engine pipeline run /path/to/spring-repo --out-dir pipeline-artifacts
doc-engine certification verify pipeline-artifacts/certification.json
```

Architecture (kernel vs adapters): [`docs/product-architecture.md`](docs/product-architecture.md).  
First real-repo run: [`docs/guides/operator-pilot.md`](docs/guides/operator-pilot.md).  
Org rollout: [`docs/guides/principal-adoption.md`](docs/guides/principal-adoption.md).

## Pipeline

```
Stage 0  Deterministic scan (no LLM)     spring_signal_scan + partition_repo + build_cross_group_edges
Stage 1  Parallel file summarization      file-summarizer × N groups
Stage 2  Parallel architecture            architect-segment × N → architect-merge
Stage 3  Gaps + review + interview        gap-analyzer + software-architect-and-testing
                                           → orchestrator asks gap questions live
Stage 4  Parallel doc generation          doc-writer × 14 files
```

Generated set: `readme`, `architecture`, `integrations`, `authorization`, `database`, `operations`, `observability`, `troubleshooting`, `configuration`, `change_impact`, `glossary`, `local_development`, `testing`, `known_limitations` (under the run’s docs dir; root `README.md` is never clobbered).

Claims are tagged **evidenced**, **confirmed**, or **unknown** so gaps stay visible. Taxonomy: [`adapters/claude/skills/document-spring-repo/references/doc-taxonomy.md`](adapters/claude/skills/document-spring-repo/references/doc-taxonomy.md).

## Stage 0 (deterministic scan)

Default scanners: `filesystem` + `ast-grep` (no Java build). Opt into CodeQL with `--scanners filesystem,codeql` when the CLI and a build command are available — see [`CONSTRAINTS.md`](CONSTRAINTS.md).

```bash
pip install -r requirements.txt   # pins ast-grep-cli, sqllineage, pathspec
python -m doc_engine.tools.spring_signal_scan <repo> --out spring_signals.json
python -m doc_engine.tools.spring_drift_check <repo> spring_signals.json --out drift_report.json
```

Rules: `src/doc_engine/scanning/resources/spring_ast_grep_rules.yml`. Fixtures: `scripts/fixtures/spring_signals/`. Target-repo `.doc-engine.yml` is **untrusted by default** (`--trust-repo-config` / `--allow-codeql-build` are explicit opt-ins).

## Quality gates and CI

Contributor policy and the full gate table live in [`CONTRIBUTING.md`](CONTRIBUTING.md). Summary:

| Gate | Hard floor / policy |
|------|---------------------|
| Whole-repo Cover% (`doc_engine` + `stf`) | **98.7** (`pyproject.toml` `fail_under`) |
| New-code coverage | **98.7** via `diff-cover` in `quality-gates` |
| Duplication (changed Python) | **≤3%** jscpd |
| Cognitive complexity | **≤5** / function (complexipy offender ratchet) |
| File size | **≤225 LOC** hard (`doc-engine size-ratchet` on `src/` + `tests/`) |
| Import cycles | tach `forbid_circular_dependencies` |
| Package layout | named concepts — **no** `utils/` / grab-bag `helpers` |

```bash
pip install -r requirements-dev.txt && pip install -e .
npm ci
doc-engine coverage-measure          # single-tree wipe + pytest-cov + path cohesion + gap-average
doc-engine quality-gates --compare-ref origin/main
doc-engine size-ratchet
```

CI (`.github/workflows/ci.yml`): Python **3.10–3.12** matrix; **only 3.11** runs pytest-cov / `fail_under` / `coverage.xml` upload. SonarCloud is a non-blocking dashboard signal; in-repo `quality-gates` is the SoT.

Mutation taxonomies (gate mutators ≠ formatting perturbations ≠ assertion-engine mutants): see CONTRIBUTING — do not conflate with PIT-style SUT mutation.

## Coverage oracle vs climb

- **Oracle / merge gate:** full-suite cohesive `coverage.xml` from one checkout (`doc-engine coverage-measure`), floor **98.7**.
- **Climb inventory:** `doc-engine coverage-gap-average` reports only files still below the floor.
- **Scoped / dual-mode measure** (fast inner loop vs full oracle): design-only — see [`docs/design/coverage-measure-modes-design-2026-08-08.md`](docs/design/coverage-measure-modes-design-2026-08-08.md). Not implemented until that memo is confirmed.

## Local orchestration and contracts

```bash
python -m doc_engine.tools.validate_artifacts --all <run-directory>
python -m doc_engine.tools.pipeline_validators <run-directory> --target-repo <repo_path>
python -m doc_engine.pipeline.local_runner /abs/path/to/spring-repo   # generative stages mocked
```

Schemas: `scripts/schemas/`. Stage graph: `src/doc_engine/pipeline/README.md`.

## Docs map

| Path | Role |
|------|------|
| [`docs/product-architecture.md`](docs/product-architecture.md) | Kernel / adapters / A+C |
| [`docs/design/`](docs/design/) | Design SoR + dated ADRs (not under `claude/`) |
| [`docs/guides/`](docs/guides/) | Operator and adoption guides |
| [`CONSTRAINTS.md`](CONSTRAINTS.md) | Runtime prerequisites and standing limits |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Write-then-verify, gates, size, mutation scopes |
| [`STATUS.md`](STATUS.md) | Current done/pending snapshot |
| [`MATURITY_ASSESSMENT.md`](MATURITY_ASSESSMENT.md) | Adoption scorecard |

## Install notes

**Kernel:** `pip install -r requirements.txt && pip install -e .`  
**Claude adapter (optional):** install via the marketplace entry that points at `adapters/claude/` — see [`docs/guides/operator-pilot.md`](docs/guides/operator-pilot.md).  
Example target config: [`docs/examples/.doc-engine.yml`](docs/examples/.doc-engine.yml).

Before production use: confirm plugin license fields still match root `LICENSE` (MIT), put `ast-grep` on `PATH` from the pinned requirements, and pilot on one smaller service first.

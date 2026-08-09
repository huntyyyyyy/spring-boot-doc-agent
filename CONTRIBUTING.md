# Contributing

## Local pre-PR gate (principal-engineer push hook)

Before opening a PR, push is the practical choke point (`gh pr create` cannot be
hooked by git). Enable the committed hooks once per clone:

```bash
git config core.hooksPath .githooks
```

`.githooks/pre-push` runs `python scripts/ci/pre_pr.py --auto` (path-risk
routing over the same hard suites CI runs). Details and tiers:
[`scripts/README.md`](scripts/README.md).

When GitHub Actions is unavailable, use
`python3 scripts/ci/pre_pr.py --actions-outage` for hermetic CI parity (CodeQL +
certification verify); procedure under **Actions outage** in
[`scripts/README.md`](scripts/README.md). That receipt is interim — re-run CI on
the same SHA when Actions recovers.

Emergency bypass (always logged under `.git/pre-pr-bypass.log`):

```bash
PRE_PR_SKIP=1 PRE_PR_SKIP_REASON='short justification here' git push
```

`PRE_PR_SKIP` alone is rejected. Prefer fixing the failing suite.

## Write-then-verify: never trust a write tool's success response alone

**Rule:** after any file write made through a device bridge, remote tool, or subagent whose only view of the filesystem is a bridged connection, the very next action is re-reading that file's actual content directly. A "written" response, a byte count, or a reported mtime is not evidence the live file changed — only a direct re-read is.

**Why this rule exists, not just what it says:** this repo has two confirmed, independent incidents of the same failure shape — trusting a tool's or document's account of state instead of re-verifying it directly:

1. A cloud sandbox session driving this repo through a device-file-bridge tool had that bridge repeatedly report a file as "written" when the live copy on disk hadn't actually changed. Caught only by re-reading the file's actual bytes after a "success" response, and re-discovered more than once because each new session initially trusted the tool's own response instead of checking. The early PR #1 write-then-verify origin story lives in git history, not as a live SoT.
2. A later, unrelated incident: a memoryless session trusted a handoff document's stale claim about repo state (that certain files were still untracked) rather than checking actual repo state (`git status`, `gh pr view`) directly, and committed files onto the wrong branch as a result. Logged in `claude/session-log.md` (2026-07-23, "Stray scaffolding commit landed on the wrong branch").

Same root cause both times — trusting a tool's or a document's *report* of state instead of the state itself — different surface (file content vs. git/PR state). The rule below is written broadly enough to cover both.

**How to apply it:**

- Local filesystem calls made directly by a Claude Code CLI session against a repo checked out on that same machine (the normal case for this repo) are not the failure mode described above — there is no bridge in that path. The rule exists for the cases that *do* have an intermediary: a device bridge, a remote/cloud sandbox tool, or any handoff where one session's account of "this is done" is the only thing a later session has to go on.
- Before treating any prior session's, document's, or tool's claim about current repo state as fact — "this file was already fixed," "these files are untracked," "this test suite passes" — re-check it directly (`git status`, a direct file read, an actual test run) rather than building further work on top of an unverified claim. Do not assume a prior session's baseline is already live; diff and confirm first.
- If you are automating verification (rather than doing it by hand) inside this repo's own Claude Code plugin tooling, the supported mechanism is a `PostToolUse` hook matched against `Write|Edit` (see `code.claude.com/docs/en/hooks` and `plugins-reference`'s hook-matcher documentation) — Claude Code's own docs don't document any built-in guarantee that a write tool's reported success reflects the live file, so a hook is the place to add that guarantee yourself if you need it enforced automatically rather than as a manual checklist step. No such hook exists in this repo as of this writing; this paragraph documents the mechanism, not a claim that it's wired in.

Research note (per `claude/steering-prompts/05-clarity-delivery-trust-research-prompt.md`): a GitHub search for small, well-maintained "write-then-verify" or checksum-confirm utilities turned up nothing genuinely on-point — the closest matches (`teran/checksum`, `nicjansma/checksum-verifier`, and similar) solve a different problem (verifying a *downloaded* file's integrity against a known-good checksum), not "did my own write tool's success response reflect what's actually on disk." Per the shared research standard, finding nothing better than "read the file back after writing it" is itself a valid result — that's the rule stated above, codified as an explicit checklist step rather than left as tribal knowledge.

## Module docstrings: reference first, rationale second

**Rule:** a module docstring opens with one sentence saying what the module *is*, then — for any
module with a `__main__` entry point — a `Usage:` block within the first 15 lines. Everything else,
including the full argument for why the module exists, goes *after* that. Comments follow the same
shape: one line saying what the code does, then the justification.

**Why this rule exists, not just what it says:** the reasoning in this repo's scripts is genuinely
valuable and is *not* the problem. Measured across `scripts/` on 2026-07-25: 35 module docstrings,
1,481 lines, mean 42. `spring_drift_check.py` ran to 202 lines with its `Usage:` block at **line
193**; `spring_signal_scan.py` to 152 lines with no usage block at all. Nine modules had none;
fourteen buried it past line 20. Someone who just wants to run the thing reads an essay first.

The density itself is deliberate and worth keeping — `.ruff.toml` sets the line limit from this
repo's own distribution precisely because 38–54% of the larger modules is explanatory prose. **This
rule deletes no reasoning.** It orders it: the reader gets a hook to hang the argument on before the
argument arrives. A skimmer reads line one and leaves; a deep reader keeps going and finds
everything that was there before.

**How to apply it:**

- Order is `what` → `how to run` → `why`. The `WHY THIS EXISTS` heading already used by
  `check_pipeline_output.py` and `check_code_quality.py` is the right marker for the third part.
- **Library modules with no CLI are exempt from the `Usage:` requirement** and should not invent one.
  `doc_tag_utils.py`, `_shared_excludes.py`, `_config_keys.py` and `_secret_heuristics.py` are
  imported, never run; demanding a usage block from them would be a check pointed at the wrong thing.
- Lead a comment with what it does, then justify: `# `bare` matches unbackticked repo paths.` before
  the paragraph explaining which incident made that necessary. The justification is why the comment
  survives review; the summary line is why anyone can skim past it.
- This is enforced, not merely encouraged: `scripts/ci/check_code_quality.py` fails when a module with a
  `__main__` entry point has no `Usage:` block near the top. It ratchets against
  `scripts/ratchets/code_quality_baseline.json`, so modules that predate the rule are recorded rather than
  blocking, and no *new* violation can land.

**On the "near the top" number, and re-deriving it.** `USAGE_WITHIN_LINES = 20` was read off this
repo's own distribution, which is bimodal: twelve modules state the command by line 18, thirteen bury
it at line 29 or later, and nothing sits in between. In the threshold-derivation literature's terms
that is *unsupervised natural-breaks clustering on a single system* — the weakest available basis.
The canonical unsupervised method (Alves, Ypma & Visser, ICSM 2010) aggregates across a benchmark of
~100 systems precisely because single-system thresholds are unstable; supervised methods key the
cut-point to a measured outcome, which needs labels this repo does not have.

So the number is a fact about the current tree, not a constant. **Re-derive it when the tree changes**
rather than defending it:

```bash
python - <<'PY'
import ast, pathlib, re
U = re.compile(r"^\s*(usage|run with|run)\s*:", re.I)
pos = []
for p in sorted(pathlib.Path("scripts").glob("*.py")):
    doc = ast.get_docstring(ast.parse(p.read_text(encoding="utf-8")))
    if not doc:
        continue
    for i, line in enumerate(doc.splitlines()):
        if U.match(line):
            pos.append(i + 1)
            break
print(sorted(pos))
PY
```

Look for the gap; put the threshold inside it. If the distribution stops being bimodal, this check
has stopped measuring something real and should be reconsidered rather than retuned.

## Line coverage ratchet

CI measures statement+branch coverage for the installable packages `doc_engine`
and `stf` (not `scripts/` or `adapters/`) and fails if the combined total drops
below `[tool.coverage.report] fail_under` in `pyproject.toml`. Ratchet upward by
editing that one number after a deliberate coverage gain. Delete local
`.coverage*` files before measuring if you previously collected statement-only
data — mixing them with `branch = true` makes coverage refuse to combine.

### One checkout, one measure (no cross-worktree combine)

Coverage DBs and `coverage.xml` are **single-writer, per-worktree** artifacts
(gitignored). Agents and humans must **never**:

- run `coverage combine` across sibling worktrees (`wt-cov-*`, `wt-complexity-*`, …)
- copy or merge `.coverage*` / `coverage.xml` from worktree A into worktree B
- compute gap-average against an XML whose `filename` paths escape the active
  checkout (absolute paths into another tree, `wt-cov-*` segments, `..` climbs)

`doc-engine coverage-gap-average` **refuses** non-cohesive reports (exit 2). Prefer
the single entry point that wipes cwd-local artifacts, runs **one** pytest+cov,
validates path cohesion, then prints gap-average:

```bash
doc-engine coverage-measure
```

CI mirrors this contract: **only the Python 3.11 matrix cell** runs
pytest-cov / `fail_under` / `coverage.xml` upload; 3.10 and 3.12 run plain
pytest for ABI signal. Do not treat a retrieved/stale artifact or a partial
worktree measure as the Cover% oracle — measure fresh in one tree.

Do not weaken `[tool.coverage.report] fail_under` (**98.7**). coverage.py's
`relative_files = true` only relativizes paths under the **current working
directory** at collection time; paths from adjacent worktrees stay absolute and
`combine` will silently union them — that is the dilution failure mode this
guard exists to catch ([coveragepy#1647](https://github.com/nedbat/coveragepy/issues/1647),
[coveragepy#1674](https://github.com/coveragepy/coveragepy/issues/1674);
DeepWiki on path normalization: [feldroy/air coverage](https://deepwiki.com/feldroy/air/4.4.2-coverage-requirements)).

Locally (after `pip install -r requirements-dev.txt` and `pip install -e .`):

```bash
# Preferred (wipe + one run + cohesion check + gap-average):
doc-engine coverage-measure

# Manual equivalent (still: one tree only; never combine across worktrees):
rm -f .coverage .coverage.* coverage.xml
pytest tests/ -q --cov=doc_engine --cov=stf --cov-branch --cov-report=term-missing --cov-report=xml
```

CI also uploads `coverage.xml` from the Python 3.11 matrix cell. The hard
**Coverage on New Code** gate is `diff-cover` in the `quality-gates` job (below),
not SonarCloud. The overall `fail_under` floor (**98.7**, same as new-code
diff-cover) stays separate from Sonar's Free QG.

### Oracle vs Climb vs Gap vs diff-cover

Approved Spec: [`docs/design/coverage-measure-modes-design-2026-08-08.md`](docs/design/coverage-measure-modes-design-2026-08-08.md)
(decisions **1–31**, artifact policy **16-A**). Climb Cover% is **not** proof of the
repo floor.

| Signal | Artifact / command | Role |
| --- | --- | --- |
| **Oracle** (SoT) | `doc-engine coverage-measure` (default `--mode oracle`) → `coverage.xml` | Whole-repo `fail_under` (**98.7**); only merge Cover% SoR |
| **Climb** (sensor) | `coverage-measure --mode climb --scope <pkg>` → `coverage.climb.xml` | Scoped accelerator only; banner `mode=climb (not CI oracle)`; **never** claims floor |
| **Gap-average** (derived) | `coverage-gap-average` on cohesive **`coverage.xml` only** | Below-floor climb inventory; green files excluded |
| **diff-cover** | `quality-gates` new-code gate | Changed-lines **98.7**; not climb inventory |

```bash
doc-engine coverage-measure
doc-engine coverage-measure --mode climb --scope doc_engine.ci
doc-engine coverage-gap-average --coverage-xml coverage.xml --worst 15
```

`below_floor_cover` is the weighted statement+branch Cover% over the below-floor
set only; `below_floor_mean_file` is the unweighted mean of those file percents.
Drive coverage-climb tests at the worst below-floor files first.

### Climb Archive / adequacy witness (Q2)

Cover% and gap-average measure **execution footprint**, not discriminative
power. Spec: [`docs/design/test-adequacy-markers-design-2026-08-09.md`](docs/design/test-adequacy-markers-design-2026-08-09.md)
(policies **Q1–Q8**). CI prints hermetic adequacy sensors via
`scripts/ci/adequacy_summary.py` (structural / mutator survivors / metamorphic
pointers) — those rows never claim the oracle floor.

When a climb batch raises Cover% on package **P**, Archive requires naming a
**witness** that bites **P**:

1. **Incident mutant** (gate mutator and/or assertion-driver mutant scoped to P), and/or
2. **mutmut slice** on the pure-Python surface under P, and/or
3. **Metamorphic relation** (Arm-1 / harness vacuity) that would fail if P’s
   asserts were vacuous

**Gap-average green alone is not Archive proof.** Clearing below-floor files
without a witness is coverage inflation, not adequacy. Mutation-scope taxonomies
(Q3) stay three mechanisms — see “Mutation-scope taxonomies” below; do not fold
them into one PIT/mutmut zoo, and do not flip suite-wide `ENFORCE=True` without
a defended Spec amendment (Q8).

| Batch | Package / modules | Witness kind | Note |
| --- | --- | --- | --- |
| B4 | `doc_engine.tools` — `spring_drift_tier2`, `spring_drift_check`, `run_manifest` | `mutmut_slice` | Tools/telemetry surface — not scan formatting; Arm-1 not cited |

### Oracle remesure cadence (saliency)

Full-suite oracle is expensive. Remesure `coverage.xml` only on **salient**
triggers (decisions **5** / **26**), not every micro-edit:

1. After a climb batch that changed production or test code you intend to merge
2. Before opening / updating a PR that touches Cover% SoT or below-floor files
3. When gap inventory is empty, clearly stale, or was built from another checkout
4. After rebasing onto a tip that changed measured packages

Between those triggers, use `--mode climb --scope <pkg>` for local feedback.
Climb exit codes mirror pytest health; they never encode the repo floor.

### Spec-driven delivery (one stream)

For coverage SoT / dual-mode / gate changes: **Spec → Implement → Verify →
Archive** with **one active tip writer** on the wave1 branch that owns
`MeasureRun` / PathCohesion (decision **21**). Do not open parallel SoT-forking
side branches or force-push tip thrash to “recover” a race. Prefer OpenSpec-style
deltas; do not adopt Spec Kit WorkflowEngine as a mandatory runtime.

### Hard refuse (coverage / quality SoT)

These are merge-policy refusals, not style preferences (synthesis Embody/Adopt/
Refuse + decisions **19–20**, **25**, **29**):

| Refuse | Why |
| --- | --- |
| Scoped climb Cover% as proof of whole-repo **98.7** | Different pytest-cov predicate |
| LLM-as-judge / advisory sensors as `fail_under` substitute | Sensors ≠ boolean merge SoT |
| Fuzzy / PID / “confidence of green” on the oracle floor | Hard predicates stay hard |
| Cross-worktree `coverage combine` or promoting `coverage.climb.xml` to SoR | Dual-write / path dilution |
| Ungated rewrite of `CONSTRAINTS.md`, coverage baselines, or `fail_under` | Needs human + claims/ratchet |
| In-tree Rust / WASM hot path by default | See [rust-stack-fit memo](docs/design/rust-stack-fit-memo-2026-08-08.md) — profiled exception only |

Only CONTRIBUTING / CI hard gates are merge SoT. Climb Cover%, gap-average,
LLM-judge, Recall@K, and carbon metrics are **sensors** — never silent
promotions.

## CI layering (E-CI / policy C-A)

`.github/workflows/ci.yml` is an **orchestration-only caller** (≤200 LOC):
triggers, permissions, concurrency, and `uses:` edges. Bounded CI contexts live
in reusable workflows:

| Workflow | Owns |
| --- | --- |
| `python-gates.yml` | install/lint/claims/markers/rule coverage + 3.11 `coverage.xml` oracle |
| `abi-tests.yml` | domain ABI shards (policy T-A; never writes coverage) |
| `codeql-signals.yml` | CodeQL pack invariants / compile / fixture runtime (+ bundle pin) |
| `quality-gates.yml` | hard in-repo gates after downloading `coverage-xml` |
| `sonar.yml` | soft SonarCloud signal (`continue-on-error` on the called job) |

Step bundles stay in-repo under `.github/actions/` (e.g. `setup-python-repo`).
Gate *logic* stays in `scripts/ci/` / `doc-engine` CLIs — no inline
`python <<'PY'` heredocs in workflows. `scripts/ci/check_workflow_yaml.py`
enforces parse/security plus LOC/heredoc SoT (`doc_engine.ci.workflow_size`).

## In-repo quality gates

SonarCloud **Free** cannot customize Quality Gate thresholds. Policy is enforced
in GitHub Actions by the `quality-gates` reusable workflow (called from
`ci.yml` after `python-gates` publishes `coverage-xml`). Logic lives in
`src/doc_engine/ci/` (installed console CLI); `scripts/ci/` keeps thin
deprecated shims only (plus CI meta gates such as `check_workflow_yaml.py`).

### Evidence table (2026-qualified tools only)

Audited against GitHub/PyPI on 2026-08-08. Rejected without 2026 push **or**
release: radon, xenon, Melevir/`cognitive_complexity`, and other pre-2026
zombies. Metric research framing: Campbell cognitive complexity (TechDebt 2018);
empirical understandability work on arXiv ([2007.12520](https://arxiv.org/abs/2007.12520),
[2303.07722](https://arxiv.org/abs/2303.07722)); coupling/churn/bus-factor as
review concerns ([2310.03673](https://arxiv.org/abs/2310.03673),
[2401.03303](https://arxiv.org/abs/2401.03303)).

| Gate | Tool | Stars (≈) | Latest release | Last push | Metric type | CI behavior |
| --- | --- | --- | --- | --- | --- | --- |
| New-code coverage ≥ **98.7%** | [diff-cover](https://github.com/Bachmann1234/diff_cover) `~=10.5.0` (+ pytest-cov XML) | 843 | **v10.5.0** (2026-08-08) | 2026-08-08 | Diff line coverage vs compare ref | **hard fail** |
| Duplication ≤ **3%** | [jscpd](https://github.com/kucherenko/jscpd) `@5.0.14` via local `npm ci` | 5980 | **v5.0.14** (2026-07-27) | 2026-08-07 | Token clone % on **changed** `src/doc_engine` + `src/stf` `.py` | **hard fail** |
| Complexity ≤ **5** / function | [complexipy](https://github.com/rohaquinlop/complexipy) `~=6.2.0` | 748 | **6.2.0** (2026-07-23) | 2026-08-04 | Cognitive complexity (Campbell/Sonar-inspired; not affiliated with Sonar) | **hard fail** on offender-count ratchet (`scripts/ratchets/complexipy_baseline.json`) until count reaches 0 |
| File / function size | in-repo `doc-engine size-ratchet` (+ `check_code_quality.py` statement growth) | — | — | — | File LOC hard **>225**; function statements hard **>50** (soft advisory **>150** LOC / **>20** stmts). Prefer files ≤225 LOC and one-screen functions | **hard fail** via `scripts/ratchets/size_baseline.json` (offender maps must not rise/grow); statement *growth* also hard in `check_code_quality.py` |
| Import cycles / coupling | [tach](https://github.com/tach-org/tach) `~=0.35.0` | 2785 | **v0.35.0** (2026-05-12) | 2026-06-11 | `forbid_circular_dependencies` (`tach.toml`) | **hard fail** |
| Soft McCabe backup | [ruff](https://github.com/astral-sh/ruff) C901 (already pinned `~=0.16.0`) | 49k+ | 2026 releases | 2026-08-08 | Cyclomatic (McCabe) — **not** cognitive | optional / not selected in `.ruff.toml` |
| Security signal | Semgrep + CodeQL (existing CI jobs) | — | — | — | SAST | unchanged hard jobs |
| SonarCloud | scanner job kept | — | — | — | Dashboard signal | **non-blocking** (`continue-on-error`) |

**import-linter** also 2026-PASS (PyPI 2.13 uploaded 2026-07-03; push 2026-08-07) but is not wired — tach alone owns the cycle gate.

**Complexity remediation.** Policy target is ≤5 cognitive complexity per function on all of `src/doc_engine` + `src/stf`. While legacy offenders remain, CI hard-fails when the offender *count* rises vs `scripts/ratchets/complexipy_baseline.json` (ratchet downward after each remediation batch; never raise it). Prefer named helpers and early returns over micro-fragmentation; do not weaken the ≤5 threshold.

**Size remediation.** Prefer files at or under **225 LOC** and functions that fit one screen (~20–50 statements). Soft advisories print above 150 LOC / 20 statements; hard ceilings are file LOC **>225** and function statements >50 under `src/doc_engine`, `src/stf`, **and `tests/`** (`doc-engine size-ratchet`, baseline `scripts/ratchets/size_baseline.json` — never raise offender maps). The same cohesion bar applies to tests: split along fixtures vs cases, domain suites, and concept-named `tests/support/…` packages — not `part2` chops or a `tests/utils` grab-bag. Remediations must be intentional design (SRP / DDD boundaries, ports-adapters, registries) — not mechanical line chops or grab-bag `utils`/`helpers` modules. Separately, `scripts/ci/check_code_quality.py` hard-fails when an existing function's statement count grows or a new function exceeds 50 statements (complexity/depth there remain advisory).

### Test-suite domains (E-TEST / policy T-A)

Every `tests/**/test_*.py` declares exactly one module-level marker:

```python
import pytest
pytestmark = pytest.mark.domain_stage0
```

Catalog SoT: `doc_engine.ci.test_domain_catalog` (Spec
`docs/design/test-suite-parallel-domains-design-2026-08-08.md`). Ownership
classifier: `doc_engine.ci.test_domain_rules`. Ratchet:

```bash
python -m doc_engine.ci.test_domain_markers_check
```

**Parallel-safe** domains may run as separate ABI CI jobs. **Serial** buckets
(`domain_integration`, `domain_unclassified`) and **opt-in** (`domain_live_optin`)
stay on the serial ABI job. The **3.11 oracle** coverage cell remains a single
`pytest tests/` writer of `coverage.xml` — never shard+combine for the floor.
Do **not** enable suite-wide pytest-xdist until E-TEST2 spikes say otherwise.

Classification debt mirrors coverage gap-average: floor **98.7**. Modules still
on `domain_unclassified` are the debt inventory; once reclassified to a named
BC they **leave that inventory** and are not part of the debt set. Reclassify
by extending the rule tuple (OCP), not by editing CI expressions by hand.

**ABI path matrix (E-TEST3).** Collection directories under fat/package roots
are discovered and **grouped by parent** `domain_*` marker
(`doc_engine.ci.test_path_shards.domain_path_matrix`). The CI matrix stays
short (one row per parallel domain); each job runs `pytest <paths…> -m
<marker>`. Emission SoT: `python -m doc_engine.ci.emit_abi_matrix`. Job
definitions live in `.github/workflows/abi-tests.yml` (reusable); `ci.yml`
only calls it. Shared install boilerplate is
`.github/actions/setup-python-repo`. `tests/support/` is a shared helper
kernel and is never a shard root.

### Quality gates (all OS)

One portable entry point — same on Mac, Windows, and Linux (and in CI):

```bash
pip install -r requirements-dev.txt && pip install -e .
npm ci
# produce coverage.xml once (pytest --cov=doc_engine --cov=stf --cov-branch --cov-report=xml)
doc-engine quality-gates --compare-ref origin/main
```

- SoT is the installed package (`doc_engine.ci` + `doc-engine` console script from `pip install -e .`), not freestanding `scripts/ci` Python. Avoid adding new OS wrappers or parallel runner scripts.
- Python tools (`diff-cover`, `tach`, `complexipy`) come from `requirements-dev.txt` and are invoked via `sys.executable -m …` or the venv console script next to that interpreter — no OS-specific wrappers.
- `jscpd` is pinned in `package.json` / `package-lock.json`. After `npm ci`, the runner prefers the platform native binary under `node_modules/jscpd-*/bin/`, else `node node_modules/jscpd/run-jscpd.js`. Do **not** use ad-hoc `npx` or throwaway `.ps1`/`.sh` gate wrappers.
- Skip coverage locally with `--skip-coverage` only for debugging other gates.

### Deferred (no fake CI gates)

| Taxonomy item | Status |
| --- | --- |
| Halstead / Maintainability Index / essential complexity | **Deferred** — radon/xenon lack 2026 releases/pushes |
| Big-O time/space | **Deferred** — not statically enforceable; ADR/review |
| LCOM / full cohesion suites | **Deferred** — no 2026-maintained Python CI tool selected |
| Fan-in/out scores as thresholds | **Deferred** — tach cycles only for now |
| Code churn as bug predictor | **Deferred** — needs history heuristics, not a merge gate |
| Bus factor | **Deferred** — blame/ownership analysis ([2401.03303](https://arxiv.org/abs/2401.03303)), not CI |
| Sonar custom Quality Gate | **Deferred on Free** — cannot set 98.7% / 3% / complexity in UI |

## Mutation-scope taxonomies

This repo has **three** deliberate-defect mechanisms. They share vocabulary
(“mutant”, “kill”, “survivor”) but **different oracles** and must not be
conflated with each other or with PIT-class Java SUT mutation (ROR / bytecode
operator taxonomies). Do not build a PIT clone here.

| Taxonomy | Where | Oracle | Not |
| --- | --- | --- | --- |
| **Gate mutators** | `scripts/ratchets/mutate.py` + `gate_mutators.py` / `mutator_registry.py`; baseline `mutation_baseline.json` | Named suite fails after an artifact-aware defect in a sandbox | Not PIT; not Type-1 formatting edits |
| **Formatting perturbations** | `scripts/ratchets/java_perturbations.py` | Meaning-preserving Type-1 edits measure drift FP / metamorphic Arm 1 | Not PIT operators; not gate mutators |
| **Assertion-engine mutants** | `tests/spring_signals/mutation_driver.py` | Kill mutants in `check-assertions` | Not the gate harness; not Java SUT mutation |

### Incident-seeded gate mutators only

New **gate** mutators must name a real near-miss / incident class this repo
actually had or narrowly avoided (check F / Grep regain, rule-form loss,
derived-count drift, size ratchet, network deny, prompt-contract drift, …).
Each catalog entry’s `why` is that incident seed. Refuse “add ROR because PIT
has it,” refuse operator-pack growth for coverage theater, and refuse folding
formatting perturbations or assertion-engine mutants into the gate registry.
Extend the catalog via `gate_mutators.definitions` (OCP); leave `mutate.py` as
the sandboxed kill/score harness.

## Package layout: named concepts, not ``utils/``

Do **not** add `src/doc_engine/utils/`, `util.py`, or a grab-bag `helpers.py`.
Shared primitives live in concept-named modules:

- `doc_engine.core` — walk/indexing, timeouts, excludes, JSON file I/O (`jsonio`)
- `doc_engine.paths` — path validation and repo/scripts layout resolution
- `doc_engine.ci` — quality-gate tooling and checkout-bound path helpers

If a helper is domain-specific (evidence tags, semantic eval, gap rates), put
it next to that domain (`tools/doc_tag_utils.py`, `scanning/gap_probe/`, …).
A new shared module must answer “what belongs here / what does not?” in its
module docstring; unexplained dumps fail review.

## SonarCloud (soft signal only)

The `sonarcloud` job still uploads analysis for the dashboard but is
**non-blocking**. Free-plan Quality Gates are not the source of truth for the
thresholds above — `quality-gates` is. Keep `SONAR_TOKEN` if you want the
dashboard; turn Automatic Analysis **OFF** if you run CI analysis (dual-method
error otherwise). `sonar.qualitygate.wait` is off in CI on purpose, and the
job uses `continue-on-error` so a Free QG miss does not fail the Actions check.

That is distinct from the **SonarQubeCloud GitHub App** check named
`SonarCloud Code Analysis`. With AA off, CI analysis still decorates the PR;
the App posts that check from the Quality Gate result. A red X there (for
example Security/Reliability Rating on New Code below A) can leave the PR
`UNSTABLE` even while `SonarCloud (non-blocking; …)` is green. Fixing that
check means clearing the Free QG findings (or dropping decoration / not
requiring the check) — toggling AA again does not remove it.

Verify AA is off: project **Administration → Analysis Method → Automatic
Analysis = OFF**. Proof CI is the only method: the `sonarcloud` job log shows
`ANALYSIS SUCCESSFUL` / `EXECUTION SUCCESS` with no
“CI analysis while Automatic Analysis is enabled” error.

In-repo Sonar parameters remain in `sonar-project.properties`
(`sonar.python.coverage.reportPaths`, coverage exclusions for `adapters/**` /
`scripts/**`, `relative_files = true` under coverage).

## Current status and steering prompts

See `STATUS.md` for a current-state snapshot of this plugin (what's done, what's pending, next concrete action) and `claude/session-log.md` for the append-only history of commits that affect the assumptions in `claude/steering-prompts/`. `CLAUDE.md` explains when a commit needs a session-log entry.

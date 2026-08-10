# Session log (nested)

Append-only record of commits that move assumptions in
`docs/process/steering-prompts/` (see `CLAUDE.md`). **Not** research SoT;
**not** a chat dump.

## Layout

| Path | Role |
| --- | --- |
| [`../session-log.md`](../session-log.md) | Stable stub (claims / old links) |
| `START__slug.md` / `START__END__slug.md` | LOC-budget shards (see naming) |
| This README | Index + append recipe + algorithm |

## Naming / sort key

Filenames are **date-first** (so `ls` stays chronological) plus a **content slug**
from the first entry title (`## YYYY-MM-DD — title` → kebab-case):

| Pattern | When |
| --- | --- |
| `YYYY-MM-DD__topic-slug.md` | Single-day shard |
| `YYYY-MM-DD__YYYY-MM-DD__topic-slug.md` | Multi-day pack |
| `…__topic-slug-2.md` | Collision on the same span+slug |

The slug is a look-first hint, not a full abstract — open the file for entries.

## Packing algorithm

**Target:** each shard ≤ **225** lines (header + entries).

1. Parse entry blocks at `## YYYY-MM-DD` (**preserve original order**).
2. **Greedy pack:** add the next entry while
   `header_lines + sum(entry_lines) ≤ 225`.
3. If the next entry would exceed the budget, flush and start a new shard.
4. Never split an entry. A single oversize entry may exceed the target alone.
5. **Name** with date-first span + first-entry **content slug** (`START__slug.md`).

Month/week calendars alone are **refused** as the size SoT.

Maintainer re-pack: `python3 scripts/process/pack_session_log.py`
(`--from-git HEAD:docs/process/session-log.md` for monolith rebuild;
`--index-only` after appending to an existing shard). Chronology SoT for
re-reads is `session-log/.pack-order` (not `ls` alpha).

## Shards (live)

| File | Span | Lead title | Entries | Lines |
| --- | --- | --- | ---: | ---: |
| [`2026-07-23__stray-scaffolding-commit-landed-on-the-wrong.md`](2026-07-23__stray-scaffolding-commit-landed-on-the-wrong.md) | 2026-07-23 → 2026-07-23 | Stray scaffolding commit landed on the wrong branch, caught by a later session | 5 | 195 |
| [`2026-07-23__2026-07-24__add-scripts-test-pipeline-stages-py-structural.md`](2026-07-23__2026-07-24__add-scripts-test-pipeline-stages-py-structural.md) | 2026-07-23 → 2026-07-24 | Add scripts/test_pipeline_stages.py (structural tests for the four LLM stages) | 4 | 199 |
| [`2026-07-24__2026-07-25__add-skills-semantic-pipeline-eval-skills.md`](2026-07-24__2026-07-25__add-skills-semantic-pipeline-eval-skills.md) | 2026-07-24 → 2026-07-25 | Add skills/semantic-pipeline-eval/, skills/capacity-preflight/, and MATURITY_ASSESSMENT.md | 4 | 191 |
| [`2026-07-25__add-scripts-check-llms-coverage-py-backfill.md`](2026-07-25__add-scripts-check-llms-coverage-py-backfill.md) | 2026-07-25 → 2026-07-25 | Add scripts/check_llms_coverage.py; backfill claude/llms/pr-9..15.md; fix stale pr-13.md | 4 | 187 |
| [`2026-07-25__spring-drift-check-py-reject-an-unfinished.md`](2026-07-25__spring-drift-check-py-reject-an-unfinished.md) | 2026-07-25 → 2026-07-25 | spring_drift_check.py: reject an unfinished/empty run_manifest.json as --manifest baseline | 5 | 219 |
| [`2026-07-24__fix-the-renumbering-breakage-in-steering.md`](2026-07-24__fix-the-renumbering-breakage-in-steering.md) | 2026-07-24 → 2026-07-24 | Fix the renumbering breakage in steering prompts 10-12; unstale CLAUDE.md's prompt count | 3 | 203 |
| [`2026-07-24__correct-the-mirror-back-scope-and-record-what.md`](2026-07-24__correct-the-mirror-back-scope-and-record-what.md) | 2026-07-24 → 2026-07-24 | Correct the mirror-back scope, and record what actually needs mirroring | 2 | 187 |
| [`2026-07-25__delete-verify-llms-docs-py-markdown-bash-c.md`](2026-07-25__delete-verify-llms-docs-py-markdown-bash-c.md) | 2026-07-25 → 2026-07-25 | Delete verify_llms_docs.py: markdown?`bash -c` execution with GH_TOKEN in CI | 2 | 151 |
| [`2026-07-25__pipeline-subagents-had-no-write-access-so-every.md`](2026-07-25__pipeline-subagents-had-no-write-access-so-every.md) | 2026-07-25 → 2026-07-25 | Pipeline subagents had no Write access, so every stage's output round-tripped through the orchestrator's context | 2 | 163 |
| [`2026-07-25__2026-07-24__replace-stage-1-s-broadcast-of-the-references.md`](2026-07-25__2026-07-24__replace-stage-1-s-broadcast-of-the-references.md) | 2026-07-25 → 2026-07-24 | Replace Stage 1's broadcast of the references bucket with a deterministic partitioned join | 2 | 211 |
| [`2026-07-24__make-spring-signals-json-byte-deterministic.md`](2026-07-24__make-spring-signals-json-byte-deterministic.md) | 2026-07-24 → 2026-07-24 | Make `spring_signals.json` byte-deterministic: sort `entity_table_map`, resolve class-name collisions on file path | 2 | 187 |
| [`2026-07-24__kitchen-sink-end-to-end-suite-three-real-bugs.md`](2026-07-24__kitchen-sink-end-to-end-suite-three-real-bugs.md) | 2026-07-24 → 2026-07-24 | Kitchen-sink end-to-end suite; three real bugs found and fixed by it | 2 | 183 |
| [`2026-07-24__2026-07-25__two-live-defects-the-quality-measurement-pass.md`](2026-07-24__2026-07-25__two-live-defects-the-quality-measurement-pass.md) | 2026-07-24 → 2026-07-25 | Two live defects the quality measurement pass turned up | 2 | 179 |
| [`2026-07-25__read-the-repo-s-claims-about-itself-back-check.md`](2026-07-25__read-the-repo-s-claims-about-itself-back-check.md) | 2026-07-25 → 2026-07-25 | Read the repo's claims about itself back: check_repo_claims.py, verify: predicates, derived: blocks | 2 | 215 |
| [`2026-07-25__measure-tier-2-s-false-positive-rate-before.md`](2026-07-25__measure-tier-2-s-false-positive-rate-before.md) | 2026-07-25 → 2026-07-25 | Measure tier 2's false-positive rate before adding anything to it | 4 | 207 |
| [`2026-07-25__2026-07-27__add-a-sixth-pipeline-agent-software-architect.md`](2026-07-25__2026-07-27__add-a-sixth-pipeline-agent-software-architect.md) | 2026-07-25 → 2026-07-27 | Add a sixth pipeline agent, software-architect-and-testing, reviewing the target repo through DDIA/Effective-Software-Testing lenses, plus a curated semgrep ruleset | 3 | 219 |
| [`2026-07-27__build-file-structural-signals-gradle-groovy.md`](2026-07-27__build-file-structural-signals-gradle-groovy.md) | 2026-07-27 → 2026-07-27 | Build-file structural signals (Gradle/Groovy/Maven/version catalogs) close CONSTRAINTS §11 | 4 | 195 |
| [`2026-07-28__pipeline-b-a-close-out-contracts-validators.md`](2026-07-28__pipeline-b-a-close-out-contracts-validators.md) | 2026-07-28 → 2026-07-28 | Pipeline B+A close-out: contracts, validators, orchestrator, repo hygiene | 5 | 215 |
| [`2026-07-28__2026-07-29__principal-review-follow-up-certified-ci.md`](2026-07-28__2026-07-29__principal-review-follow-up-certified-ci.md) | 2026-07-28 → 2026-07-29 | Principal review follow-up: certified CI, partition/write-scope fixes, module split | 5 | 215 |
| [`2026-07-29__ci-workflow-yaml-parse-gate-next-arc-fact-store.md`](2026-07-29__ci-workflow-yaml-parse-gate-next-arc-fact-store.md) | 2026-07-29 → 2026-07-29 | CI workflow YAML parse gate; next arc = fact-store Phase 1 | 5 | 195 |
| [`2026-07-29__2026-07-30__scope-clarity-cleanup-post-packaging-docs-dead.md`](2026-07-29__2026-07-30__scope-clarity-cleanup-post-packaging-docs-dead.md) | 2026-07-29 → 2026-07-30 | Scope clarity cleanup (post-packaging docs + dead bootstraps) | 6 | 203 |
| [`2026-07-30__control-wiring-gates-called-by-behavior-wiring.md`](2026-07-30__control-wiring-gates-called-by-behavior-wiring.md) | 2026-07-30 → 2026-07-30 | Control-wiring gates (called_by / behavior / wiring tests) | 6 | 195 |
| [`2026-07-30__pe-pre-pr-gate-compose-rare-touches.md`](2026-07-30__pe-pre-pr-gate-compose-rare-touches.md) | 2026-07-30 → 2026-07-30 | PE pre-PR gate (compose + rare touches) | 5 | 195 |
| [`2026-07-30__un-dark-skip-drift-normalization-certification.md`](2026-07-30__un-dark-skip-drift-normalization-certification.md) | 2026-07-30 → 2026-07-30 | Un-dark-skip drift_normalization; certification Usage docstring | 8 | 215 |
| [`2026-07-30__2026-08-08__post-merge-status-constraints-l2b-next-l4-still.md`](2026-07-30__2026-08-08__post-merge-status-constraints-l2b-next-l4-still.md) | 2026-07-30 → 2026-08-08 | Post-merge STATUS/CONSTRAINTS: L2b next; L4 still human | 15 | 221 |
| [`2026-08-08__2026-08-10__size-ratchet-includes-tests-cohesive-test.md`](2026-08-08__2026-08-10__size-ratchet-includes-tests-cohesive-test.md) | 2026-08-08 → 2026-08-10 | Size ratchet includes tests/; cohesive test modularization ≤225 | 25 | 219 |
| [`2026-08-10__e-ctx0-draft-agent-context-markdown-bloat.md`](2026-08-10__e-ctx0-draft-agent-context-markdown-bloat.md) | 2026-08-10 → 2026-08-10 | E-CTX0 draft: agent context / markdown bloat research | 19 | 164 |

**Totals:** 151 entries → 27 shards; max 221 lines;
over-budget 0.

## How to append

1. Open the **latest** shard (last row above). If it is near **225** lines,
   create `YYYY-MM-DD__your-topic.md` instead.
2. Append one distilled entry at the **bottom**.
3. Do **not** rewrite older shards to tidy dates/SHAs.
4. Do **not** append to [`../session-log.md`](../session-log.md).

### Entry template

```
## <YYYY-MM-DD> — <short description>
Commit: <short sha, or "uncommitted" if writing before commit>
Tests: <pass/fail summary, or "not run">
Assumptions affected:
- `<prompt or doc>` — "<assumption>" — [Resolved — …] / [Still accurate] / [New info — …]
Files touched: <comma-separated list>
```

## Refuse

- Chat transcripts as research SoT
- Rewriting historical entries for tidy dates/SHAs
- Calendar-only splits that ignore LOC
- Reviving a multi-thousand-line `session-log.md` body

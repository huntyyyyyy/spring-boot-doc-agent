# Session log — 2026-07-25 → 2026-07-24

Lead: **Replace Stage 1's broadcast of the references bucket with a deterministic partitioned join**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-25 ? Replace Stage 1's broadcast of the references bucket with a deterministic partitioned join



Commit: 065680a



Tests: `test_build_cross_group_edges.py` 20/20 (new; 2 of them opt-in via `PIPELINE_ARTIFACTS_DIR` and verified against a real completed Stage 0). `test_pipeline_stages.py` 17/17. Full suite 331 passing, 12 skips. CI 16 ? 17 steps.



Assumptions affected:



- `skills/document-spring-repo/SKILL.md` Stage 1 ? "It's cheap ? file/line/package-or-import-text triples, not source ? so passing all of it to every dispatch should be inexpensive regardless of repo size, but this is worth confirming against a real repo's actual `references` bucket size rather than just assumed" ? [Resolved ? confirmed, and the assumption was wrong in the direction that matters. The per-row cost is indeed small; the *volume* is `g × |R|`, and both terms grow with repo size, so shipped volume is quadratic. Measured on a public 109-file sample repo: 1030 rows broadcast, 75 load-bearing. The prompt's own hedge asked for exactly this measurement; this is the answer.]



- `agents/file-summarizer.md` step 3 ? "cross-check this file's own package/import lines against the repo-wide `references` bucket's package/import entries" ? [Resolved ? deleted. That instruction was a `package`/`import` string join performed by a language model, once per group, with the whole right-hand table in context. It is now a hash join in Stage 0: build side = package declarations, probe side = imports. The subagent receives resolved arcs as ground truth, the same way it already receives the signal-scan slice.]



- `agents/file-summarizer.md` step 3's stated limits ? "a same-package reference needs no import statement at all ... so two files in the same package that landed in *different* groups won't be caught this way" ? [Resolved ? the deterministic join catches precisely this case, because a package index does not need an import to exist. On the sample repo it is the *largest* class of cross-group relationship: 47 adjacency rows against 14 import arcs. The prompt-based version could not see any of them, by its own admission.]



- `claude/10-architecture-maturation-plan.md` ? the DDIA audit annotation's gap 1, "derived data being re-derived probabilistically per worker instead of once in the system-of-record layer" ? [Resolved for this instance. One of the three gaps the audit named is closed: the cross-group relation is now computed once in the deterministic layer, exactly, and is legitimately taggable `[Evidenced ? path:line]` rather than being an LLM inference the tag grammar cannot honestly label. The other two gaps (no determinism probe, no inter-stage schemas beyond `spring_signals.json`/`run_manifest.json`) remain ? though `cross_group_edges.json` ships with a `schema_version`, which is a start.]



- `skills/capacity-preflight/SKILL.md` and `scripts/capacity_preflight.py` ? the `references_bucket_total_across_groups_est_tokens` metric and its 500k warning threshold ? [**New info ? now measures a cost the pipeline no longer pays.** It computes references-bucket-tokens × group-count, which was the broadcast volume. After this change each group receives only its own boundary. The metric is not wrong, it is stale: it will over-warn, and the number a reader should actually care about is the *cut* size. Deliberately not changed here ? picking the replacement threshold needs data from more than one repo. Flagged as the next preflight change.]







Details: new `scripts/build_cross_group_edges.py`, run in Stage 0 after both `spring_signal_scan.py` and `partition_repo.py` (it needs both, so it belongs to neither). Three correctness properties that are easy to get wrong and are each pinned by tests:







1. **The grouping is a cover, not a partition** ? `partition_repo.py` overlaps adjacent groups by ~10% of tokens, so a file can belong to two. An arc is cut iff *no* group contains both endpoints; `owner(u) != owner(v)` is ill-defined and silently wrong. A first pass at measuring this used a scalar file?group map and had to be redone.



2. **Resolve imports to a type, not a package** ? `import a.Foo` names a type; keying on the package fans out to every file in it, making the join many-to-many with output proportional to package size. Measured on the sample: package-keyed 61 arcs, type-keyed 14.



3. **Same-package is an equivalence relation, so each package induces a clique** ? materializing cross-group pairs costs `O(?|P|?)` and would dominate everything (111 pairs vs 14 arcs on the sample). Emitted as adjacency instead: per group, the package's files that live outside it. `O(|P|)`, not `O(|P|?)`.







Also fixed a resolution gap found while writing the tests: static-member and nested-class imports (`import static a.Foo.BAR`, `import a.Foo.Inner`) resolve to nothing on a single `rsplit`, and vanish silently. Handled by shortening the qualified name one component at a time until it resolves.







Why the cut stays small is a precondition worth stating rather than assuming: `partition_repo.py` is DFS-ordered and token-greedy, with no cut guarantee at all. It works because in Java packages *are* directories, so same-package files land contiguously and the densest arc class is intra-group by construction. Expect this to degrade for languages where namespace and directory are independent.







Files touched: scripts/build_cross_group_edges.py, scripts/test_build_cross_group_edges.py, skills/document-spring-repo/SKILL.md, agents/file-summarizer.md, .github/workflows/ci.yml, claude/session-log.md







## 2026-07-24 ? Close the missing-citation blind spot: carry line anchors through Stage 1, plus a coverage checker



Commit: 065680a



Tests: `test_citation_coverage.py` 34/34 (new). `test_pipeline_stages.py` 17 ? 29 (12 new: 8 for the summarizer `evidence` shape, 4 for gap-analyzer citation discipline). `test_check_pipeline_output.py` 20/20 unaffected. Full suite 307 passing, 8 skips, on this branch's base (`main`). CI 17 ? 18 steps.



Note on that number: it is measured against `main`, not against `parked-session-log-validator`, where the same tree reports 377/12 ? the 70-test difference is `test_check_session_log.py`, which lives only on that deliberately-unmerged branch. Stating the branch the count was taken on, since this repo has already been bitten once by a bare test count going stale.



Assumptions affected:



- `claude/steering-prompts/01-testability-research-prompt.md` ? "What to scaffold and implement" item 2, "**every substantive claim ends in one of the five required tags** from `doc-writer.md`'s Rule 1" ? [**New info, partially resolved** ? this specific assertion was specified in the prompt but never actually built. `test_pipeline_stages.py` and `check_pipeline_output.py` between them check tag *grammar* and citation *resolvability*, and both work by iterating tags that already exist: `find_malformed_tags()` only matches bracket spans starting with a recognized tag word, `resolve_evidenced_citations()` only iterates `TAG_PATTERNS["evidenced"]` matches. A sentence with no tag matches neither, so it was never "failing" ? it was invisible. `scripts/citation_coverage.py` now covers it. Stopping short of `[Resolved]` deliberately: the prompt asked for a structural assertion, and what landed is an artifact-gated heuristic that exits 0 by default (`--strict` opts in), because "is this sentence a substantive claim?" has no mechanical answer. It narrows where to look; it does not decide.]



- `claude/steering-prompts/01-testability-research-prompt.md` ? same item 2, "`Unknown` count doesn't silently balloon past a sane threshold" ? [Still accurate ? not addressed here. `run_manifest.json` records `evidence_tag_counts`, but nothing thresholds them. Note this interacts with the change above: A5 in the new skill tells writers to prefer `[Unknown]` over silence, which should *raise* Unknown counts by converting invisible omissions into visible gaps. A threshold added later should expect that, and not read it as regression.]



- `skills/semantic-pipeline-eval/SKILL.md` ? "samples `[Evidenced]` claims and checks the cited file:line really supports the claim" ? [Still accurate, and its complement now exists. That skill has the same tag-must-exist precondition as the mechanical gate, from the judgment side. `citation_coverage.py`'s weak-anchor check is deliberately *not* a duplicate: it asks only whether symbols the claim names appear near the cited line, never whether the claim is true.]



- `agents/file-summarizer.md`'s output schema (step 4 / the JSON block) ? carried `"file": "relative/path.java"` and prose, no line field ? [**Resolved ? and this was the actual root cause, not the checker's absence.** A static trace of all six stages settled it: `spring_signals.json` carries a `line` per hit (`spring_signal_scan.py:781`) and Stage 5 is *required* to emit `path:line`, but Stages 1?4 were all line-free by schema. So `doc-writer` could line-cite only what Stage 0's ~30 ast-grep rules mechanically matched; every claim from the semantic layer ? the summarizer's business-purpose prose, i.e. the bulk of the fourteen docs ? arrived with a path and no line. Its only exits were to re-read the file (correct, expensive, skipped under context pressure), cite file-only (structurally valid, since `doc_tag_utils.py`'s `(?::(\d+))?` makes the line optional ? and indistinguishable to a reader from a missing citation), or guess. **The reported symptom is the predicted equilibrium of the last two.** Fixed by adding an `evidence` array (`{"line": N, "what": "..."}`) to the per-file object, enforced in `test_pipeline_stages.py`'s `required_keys`. Stage 1 is the only stage holding both the open file and the semantic claim, so it is the sole point where the anchor is recoverable at near-zero marginal cost ? after it, the information is simply gone.]



- `agents/gap-analyzer.md`'s `evidence` field ? unconstrained prose, and its own canonical example shipped `(src/.../InvoiceService.java)` ? [**Resolved** ? a second, independent hole, found by the same trace and easy to miss because it sits in the `[Confirmed]` lane rather than the `[Evidenced]` one. A gap question becomes an interview question, becomes an `interview_answers.json` entry, becomes a `[Confirmed ? interview, <date>]` claim ? the one tag whose provenance never touches code again. So this field was the only place that lane was ever anchored to a location, and it required nothing. Now requires a resolvable `path/File.java:line`, rejects elided paths specifically (the exact shape its own example modeled), and says to cite the thing that *is* there when the gap is about an absence ? an absence has no line number; the evidence for it always does.]



- `skills/document-spring-repo/SKILL.md` Stage 1 ? the enumerated per-file key list ? [Resolved ? updated in the same commit. Worth noting for the next session: this key list exists in **three** places (the agent prompt's JSON block, `SKILL.md`'s prose, and `test_pipeline_stages.py`'s `required_keys`). The test is the only one that fails when they drift, which is the argument for adding a key there first and letting the other two follow.]







Details, part 1 ? the contract change (above) is the fix; this is the backstop. New `skills/citation-coverage/` (authoring rules + detection pass) and `scripts/citation_coverage.py`. Three checks, all worklists rather than verdicts, following `semantic_eval_helpers.find_unmatched_confirmed_tags()`'s framing:







1. **`untagged_claim`** ? a sentence naming a concrete repo artifact (source path, `@Annotation`, CamelCase type, `method()`, dotted config key, `SCREAMING_SNAKE` constant) with no tag of any kind. The artifact gate is the whole false-positive story: flagging every untagged sentence buries findings under narration, so the rule is the narrowest one that still catches the defect ? *if you named a code artifact, cite where it lives*. A **malformed** tag counts as tagged here, deliberately: `find_malformed_tags()` already owns that finding, and counting it twice files one defect as two.



2. **`miscased_tag`** ? closes a hole nothing else could see. Every pattern in `doc_tag_utils.py` is case-sensitive, so `[evidenced ? Foo.java:6]` matches `TAG_PATTERNS` not at all *and* `TAG_WORD_SPAN` not at all: `find_malformed_tags()` never sees it and the counters score it as absent. A prior session named it exactly ? "a fully different casing isn't caught as malformed, it's simply invisible to a grep-shaped check." Reported as its own finding rather than folded into `untagged_claim`, since it describes a different defect: the writer did cite, and every counter in the repo disagrees.



3. **`symbol_absent_from_file` / `symbol_outside_window`** ? split rather than merged, because they have different causes. Absent-from-file is the shape of a citation invented to satisfy the grammar; outside-window is a real file with an imprecise anchor. Both are cases `resolve_evidenced_citations()` passes clean, since it only proves the path exists and the file is long enough.







Details, part 2 ? prevention. `doc-writer.md` Rule 6 now enumerates the three sources that legitimately carry a line (signal-scan hits, the new `evidence` array, a file you opened yourself) and states plainly that summary *prose* is not one of them. The skill adds rule **A8** for a hazard the transcript sweep surfaced and that no checker can catch: **the same tag names mean two different things in this repo.** The review layer (`10-review-persona-and-standards.md`) defines `[Evidenced]` as "strongly supported, one inference step short of executed proof"; `doc-taxonomy.md` means a directly-readable fact. An agent carrying the first definition into doc-writing silently converts inferences into evidence. Related observation worth keeping: a research subagent in this project's history correctly self-reported unopened sources as `PLAUSIBLE-BUT-UNVERIFIED` *only because its prompt forced a two-tier tag* ? plain `[Evidenced]` has no such forcing function.







Three prior incidents in this repo's own history motivated the specific checks, rather than them being designed from first principles: a module docstring citing `_query_citations_depending_on_entity()` and `_flag_stale_jpql_lineage()`, neither of which "has existed at any commit"; a fact genuinely present at `:201`/`:214`/`:223` cited as `:272`; and the Windows path-separator bug that left Stage 1's evidence slice empty for every dispatch with no error signal, documented in the 2026-07-25 entry above.







Two things deliberately **not** done, both stated rather than left implied. The checker is **fail-open** (exits 0 unless `--strict`) and is CI-wired only for its unit tests, because CI has no completed target-repo run to check ? the same constraint `check_pipeline_output.py` and `check_no_secrets_leaked.py` already live under. And there is still **no labeled ground-truth corpus** (`scripts/test_fixtures/` holds only `spring_signals`), so every detector's precision and recall ? including `DEFAULT_ANCHOR_WINDOW = 8`, an unvalidated constant ? are unmeasured. That is the honest reason `--strict` is not the default: an unknown false-positive rate means unknown breakage. Building that corpus from a real run is the natural next step, and it is also what would confirm or refute the root-cause claim above.







One asymmetry worth naming, since it is the root incentive problem and no checker fixes it: every tag form is auditable, and no tag is not. Omitting a tag is always the locally cheapest move and, before this change, carried no downstream consequence.







Files touched: agents/file-summarizer.md, agents/gap-analyzer.md, agents/doc-writer.md, scripts/test_pipeline_stages.py, scripts/citation_coverage.py, scripts/test_citation_coverage.py, skills/citation-coverage/SKILL.md, skills/document-spring-repo/SKILL.md, .github/workflows/ci.yml, claude/session-log.md








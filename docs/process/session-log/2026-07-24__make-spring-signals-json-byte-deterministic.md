# Session log — 2026-07-24

Lead: **Make `spring_signals.json` byte-deterministic: sort `entity_table_map`, resolve class-name collisions on file path**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 2. Newest at the bottom of this file.

---

## 2026-07-24 ? Make `spring_signals.json` byte-deterministic: sort `entity_table_map`, resolve class-name collisions on file path



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: `test_spring_signal_scan.py` 42 ? 45 (3 new). Full suite 310 passing, 8 skips on this branch (`citation-line-anchors`); 307/8 before. Both new ordering assertions were verified to **fail** against the unfixed scanner before being kept ? see the caveat below about the one that didn't.



Assumptions affected:



- `claude/steering-prompts/01-testability-research-prompt.md` ? "It has real, checked-in tests for its two deterministic scripts: `test_partition_repo.py`, `test_spring_signal_scan.py` ... **That's solid.**" ? [New info ? the coverage was real but had a hole exactly where the prompt's confidence was highest. `test_spring_signal_scan.py` asserted evidence-bucket sortedness (`test_evidence_is_sorted_for_determinism`) and nothing else about output stability, so `entity_table_map` ? the one structure in `scan()`'s output never sorted on the way out ? was unguarded. Measured, not theorized: against the unfixed scanner the fixture's key order is `['LegacyAudit', 'Invoice', 'SLARule', 'PaymentLedger']`. The prompt's framing of the deterministic scripts as the well-tested half of the repo is still broadly right, but "deterministic" was an assumed property of these scripts rather than an asserted one, and the assumption was false.]



Files touched: scripts/spring_signal_scan.py, scripts/test_spring_signal_scan.py, CONSTRAINTS.md, .gitignore, claude/session-log.md, claude/observability-provenance-adoption-plan-2026-07-24.md







`CONSTRAINTS.md` pass (per `CLAUDE.md`'s new "The same check covers `CONSTRAINTS.md`" rule), two entries under **Known precision tradeoffs**:



- **Item 2's "permanently out of scope" list** claimed `entity_table_map`'s simple-name keying means an unresolvable query "correctly reports 'not found' rather than a wrong resolution." That has an exception the entry never named: two `@Entity` classes with the same simple name in different packages collide, one wins, and a JPQL query in the loser's package resolves to the winner's table ? a wrong resolution, not a miss. Before this commit the winner was also unstable across runs. Now deterministic (lowest file path) but still arbitrary; emitting `contested` per `10-architecture-maturation-plan.md:154` is the real fix and is not built. Tagged `[New info]` rather than `[Resolved]` deliberately ? determinism is not correctness here, and reading it as resolved would be exactly the failure mode the item-46 correction below already documents.



- **New item 5** records byte-determinism as an asserted invariant rather than an assumed one, and carries the negative result about probes-versus-invariants so the next person evaluating reproducibility tooling starts from the measurement instead of the intuition.







`.gitignore` gained an ignore rule for the target checkout ? a real target service was added to the working tree this session for the first end-to-end run, and it is untracked, ~101MB, and contains a third party's internal source. This repo is public and MIT; the ignore rule is there so a stray `git add -A` cannot publish it. Note this is the mechanism `CONSTRAINTS.md`'s confidentiality rule ("real target-repo names/source must not enter this plugin's own tracked files") has relied on nothing but memory to enforce until now.







Details. Two distinct nondeterminisms in one structure, both fixed:







1. **Key order.** `entity_table_map` is populated inside the ast-grep match loop and was emitted unsorted. Every sibling structure is sorted ? the evidence buckets are re-sorted under a comment stating outright that ast-grep's multithreaded match order is not stable across runs ? so this reads as an omission, not a decision. Consequence is narrow but total: `compute_file_signature()` and every downstream hash read raw bytes, so identical scans of an unchanged repo serialized differently and a hash of `spring_signals.json` could not be used to assert anything.



2. **Collision winner.** The map is keyed by *simple* class name, so two `@Entity` classes in different packages collide, and plain last-write-wins handed the winner to that same unstable match order ? the same tree could report a different `table` for the same key on a re-scan. Now resolved on lowest file path, which depends only on the input. Note this is a behavior change, not just an ordering one: it is the only part of this commit that can change what a scan *says* rather than how it is serialized.







Both were predicted. `claude/10-architecture-maturation-plan.md:117` (item 0.3.1) called for exactly this ? "Also sort the map assignment for determinism ? today the winner depends on multithreaded ast-grep match order" ? and `:156` restates it as "deterministic ordering on emit, not only at the end of `scan()`." Deliberately **not** marking those items resolved in that document here, to keep this commit to fix-plus-tests; the plan file has its own review pass due.







One negative result worth more than the fix, recorded in the test body so it isn't rediscovered: **the naive determinism probe did not catch this.** `test_two_scans_of_the_same_tree_serialize_identically` ? run `scan()` twice, compare serialized bytes ? **passed against the unfixed scanner**, because two calls inside one process happened to observe the same ast-grep match order. The explicit sortedness assertions are what actually failed. The general lesson is that re-running and diffing is strictly weaker than naming the invariant: a probe can only catch nondeterminism that varies *within the conditions it happens to vary*, whereas `keys == sorted(keys)` is true or false on a single run. This is directly relevant to any future adoption of reproducibility tooling (`reprotest`/`diffoscope`), whose entire mechanism is the weaker of the two ? they earn their keep by varying environment (locale, timezone, filesystem order) rather than by re-running under identical conditions, and that distinction is the whole reason they'd be worth adding. The probe is kept as a broad regression net, not as the detector for this class.







Context for the next session: this commit is item A1 of `claude/observability-provenance-adoption-plan-2026-07-24.md`, which audits an external research report on observability/provenance/data modeling. That plan's premise audit is the part worth reading first ? three of the report's eight recommendations describe repo state that does not exist (notably: the `{subject, predicate, object, ...}` fact tuple is proposed at `10-architecture-maturation-plan.md:144`, not implemented anywhere, so any recommendation to profile or migrate its fields has no referent).







## 2026-07-24 ? De-stale `capacity_preflight.py`: it was measuring a broadcast removed three commits earlier



Commit: 065680a at write time ? see `git log` for this entry's commit



Tests: `test_capacity_preflight.py` 9 ? 10 (one deleted, two added). Full suite 311 passing, 8 skips on `deterministic-entity-table-map`. Verified against a real 615-file Spring service, not only the fixture.



Assumptions affected:



- `claude/steering-prompts/03-constraints-research-prompt.md` (via `CONSTRAINTS.md`'s "Known precision tradeoffs" item 3, the entry the 2026-07-25 log entry cited when `capacity-preflight` was built) ? "`capacity-preflight` turns this into a concrete, per-repo number: group count, total subagent fan-out, references-bucket-tokens × num_groups" ? [**Resolved for two of three dimensions, falsified for the third.** Group count and fan-out were and remain correct. The third measured `len(json.dumps(references)) × num_groups`, a quantity commit `abd3ade` had already eliminated by replacing Stage 1's broadcast with a partitioned join. Measured on a real service: 7,627,230 est. tokens reported against 358,645 actually shipped, ~21x, in the direction of alarm. Now measures the per-group `cross_group_edges.json` slice, reported as a distribution rather than a scalar, with the threshold keyed on `max` ? a context window is breached by one dispatch, not by a sum.]



- `claude/steering-prompts/01-testability-research-prompt.md` ? "real, checked-in tests for its two deterministic scripts ? That's solid" ? [New info, second instance this session. `test_references_bucket_tokens_scale_with_group_count` asserted that per-dispatch payload stays constant while total rises linearly with group count ? i.e. it pinned `cost = |R| × g`, the broadcast model, *as an invariant*. It kept passing after `abd3ade` because it exercised `capacity_preflight`'s own arithmetic rather than the pipeline's behavior, so it was defending code that no longer existed. Deleted and replaced with its inverse. Worth stating as a class: a test written against a consumer's internal arithmetic, rather than against the producer's contract, survives the contract changing ? and then actively resists the fix.]







Details. The stale dimension was baked into eight places (module docstring assumption 3, `_load_or_scan_references`, `estimate_references_bucket_tokens`, the `× num_groups` multiply, one warning, three report keys, one CLI flag, the summary print) plus six prose repetitions across `skills/capacity-preflight/SKILL.md`, `README.md`, and `skills/document-spring-repo/SKILL.md`.







Three deliberate choices:



1. **`max`, not `total`, carries the threshold.** The old metric was a whole-run sum because a broadcast has only one meaningful number. A partitioned payload has two, and they answer different questions: `total` is whole-run cost, `max` is whether any single dispatch fits. A test (`test_warning_keys_on_the_max_not_the_sum`) pins that many small slices summing large must *not* warn.



2. **The 500,000 default did not carry over.** It was calibrated against a quantity that no longer exists, so retuning it would have been false precision. New default is 30,000 ? a quarter of the default 120,000 per-group budget ? stated as a guess with exactly one real data point behind it.



3. **The join's own `stats` are reported through, not re-derived.** `build_cross_group_edges.build_report()` already computes `rows_shipped` vs `broadcast_rows_avoided`; preflight surfaces that block verbatim, preserving this script's stated no-second-implementation rule.







Also fixed in passing: `build_cross_group_edges.py`'s summary printed `(Nonex reduction)` for a single-group repo. `reduction_factor` is correctly `None` when nothing is shipped (a one-group repo has no cut by definition) and the JSON was always right ? only the human-readable line interpolated it. Invisible until a repo partitions to one group, which is exactly what the fixture does.







The first real-repo run is the reason all of this surfaced, and it is worth recording that it was the *cheapest* possible run ? Stage 0 only, no LLM calls, ~9 seconds ? and it still invalidated a measurement tool, a test, and six paragraphs of prose. `claude/10-architecture-maturation-plan.md:261` argues for one real run before Phase 1 on the grounds that fixture-derived evidence is thin. This is a data point for that argument that cost almost nothing to obtain.







Files touched: scripts/capacity_preflight.py, scripts/test_capacity_preflight.py, scripts/build_cross_group_edges.py, CONSTRAINTS.md, MATURITY_ASSESSMENT.md, STATUS.md, README.md, skills/capacity-preflight/SKILL.md, skills/document-spring-repo/SKILL.md, claude/session-log.md








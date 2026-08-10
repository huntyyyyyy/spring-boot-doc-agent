# Session log — 2026-08-10

Lead: **E-CTX0 draft: agent context / markdown bloat research**

Packed shard (target ≤225 lines). Index: [`README.md`](README.md).

Entries: 13. Newest at the bottom of this file.

---

## 2026-08-10 — E-CTX0 draft: agent context / markdown bloat research
Commit: 5d74cea
Tests: not run (docs-only Spec draft)
Assumptions affected:
- Bigger windows fix dumping research markdown into tips — [New info — Liu arXiv:2307.03172 U-curve; refuse as structural fix]
- LLM-summary always better than dropping old observations — [New info — Complexity Trap arXiv:2508.21433: masking ≈ summary]
Files touched: docs/research/process/26-agent-context-markdown-bloat-2026.md, docs/research/README.md, docs/research/quality-backlog.md, docs/process/session-log.md

## 2026-08-10 — E-CTX0 deepdive: models + GH star-inflation discernment
Commit: 745f158
Tests: not run (docs-only); GitHub API metrics fetched 2026-08-10
Assumptions affected:
- ★≥1k + recent push ⇒ safe research/implement SoR — [New info — He et al. arXiv:2412.13459; AI/LLM repos are fake-star targets; amend bar to filter+discernment]
- Low-★ repos cannot be algorithm SoR — [Resolved — Complexity Trap 17★ JetBrains paper preferred over viral MCP ★ for mask vs summary]
- E-STK0 memory shortlist ★ confidence — [New info — claude-mem/headroom/rtk hyper ★/day; magic-context LOW_FORK; re-score in memo 27]
Files touched: docs/research/process/27-*, 26-* (cross-link), README, quality-backlog P19, session-log

## 2026-08-10 — E-CTX0 algorithm-first: build/orchestrate from theory
Commit: 2b7d5b8
Tests: not run (docs-only Spec amend)
Assumptions affected:
- Quality comes from adopting high-★ memory products — [Resolved — doctrine: named algorithm + Accept predicate; self-orchestrated ports (memo 28)]
- Token-level prompt compressors are fine for coding agents — [New info — AGORA arXiv:2605.26596: action-grammar destruction; refuse on trajectories]
- First build target unclear — [Resolved — observation/step masking + always-keep floor; MemGPT/CAT/Liu as laws not runtimes]
Files touched: docs/research/process/28-*, 26-* verdict, README, quality-backlog P19, session-log

## 2026-08-10 — Combine E-REPO + E-CTX0 tips into one PR
Commit: 55209a7
Tests: not run (merge tip)
Assumptions affected:
- Parallel PRs #114/#115/#116 for same agent arc — [Resolved — single branch `cursor/repo-and-context-combined-83d2` supersedes]
Files touched: merge of nest + context-hygiene research

## 2026-08-10 — Merge PR #113 (local-ci-gate-fix) into combined REPO+CTX tip
Commit: b096755
Tests: not run (merge conflict resolution only)
Assumptions affected:
- `docs/research/README.md` — domain map paths (`modularity/` vs `bounded-contexts/`) — [Resolved — combined map uses `bounded-contexts/`; keeps agent context 26–28; folds #113 cold-BC / Rust / stage0 rows]
- `docs/research/quality-backlog.md` — Active tip + P-rows — [Resolved — kept #113 P-rows + REPO/CTX as P36/P37; Active tip notes combined tip]
- semantic_eval nest vs #113 tools façade — [Still accurate — package BC + tools shims + thin `tools/semantic_eval.py`]
Files touched: docs/research/README.md, docs/research/quality-backlog.md, docs/process/session-log.md, docs/research/bounded-contexts/*, src/doc_engine/tools/semantic_eval*.py

## 2026-08-10 — Merge PR #117 (problem-first RAG/DS/CLI) into combined tip
Commit: 4d3c444
Tests: not run (docs merge)
Assumptions affected:
- Parallel open PR #117 vs umbrella #119 — [Resolved — folded into `cursor/repo-and-context-combined-83d2`]
Files touched: process/20-rag-*, 39-cli-operator-*, 42-problem-first-*, coverage-quality/42-ds-mlops-*

## 2026-08-10 — Merge PR #118 (dynamics / physical computing) into combined tip
Commit: 5d6b485
Tests: not run (docs merge + backlog renumber)
Assumptions affected:
- Parallel open PR #118 vs umbrella #119 — [Resolved — folded; E-DYN1 backlog as **P38** (tip P20 already Concern→solution)]
- `docs/research/README.md` process row — [Resolved — dynamics links 05/20/21/43/45 + RAG]
Files touched: process/20-theory-*, 21-physical-*, 43–45-*, cross-domain-isomorphism skill/rule, quality-backlog P38, README

## 2026-08-10 — Reshape quality-backlog layout (Done vs Active)
Commit: 48880a5
Tests: claims OK; 4/4 `test_tools_bc_inventory` passing
Assumptions affected:
- `docs/research/quality-backlog.md` is an ordered P0…Pn ticket dump — [Resolved — Active tip + queues + Done ledger; P-tables archived]
- Start next chat at backlog P0 — [Resolved — P0 is conditional size hygiene; Active tip is land #119 then E-COH1]
Files touched: docs/research/quality-backlog.md, docs/research/archive/quality-backlog-ticket-ledger-2026-08-10.md, docs/research/README.md, docs/process/session-log.md, docs/design/tools_bc_inventory.json


## 2026-08-10 — Fast mutation_driver entrypoint probe (no kill loop in pytest)
Commit: a46221fd
Tests: 12/12 `test_mutation_driver_entrypoint` + `test_local_grading_pack` in 0.19s; claims OK
Assumptions affected:
- `tests/ci/test_mutation_driver_entrypoint.py` must run full mutant kills to lock ModuleNotFoundError — [Resolved — `--import-only` bootstrap probe; full kills stay in CI/pre_pr]
- grading-pack `self-test` should call `doctor` — [Resolved — hygiene-only; doctor remains its own id]
Files touched: tests/spring_signals/mutation_driver.py, tests/ci/test_mutation_driver_entrypoint.py, scripts/ci/grading_pack_steps.sh, docs/process/session-log.md

## 2026-08-10 — Global façade-bind gate (climb poke vs lazy _facade)
Commit: 7be43f55
Tests: 16/16 façade bind + public_surface + B7; poke/public_surface scripts green; claims OK
Assumptions affected:
- Climb setattr on `semantic_eval` reaches scan via any tools shim — [Resolved — FACADE_BINDS + public_surface hard; helpers bind fails closed]
- `PRE_PR_MODE=fast` is fine for tip push — [New info — refuse for tip; telemetry `92330ddf-fast` skipped oracle; only `--auto`/`full`]
Files touched: src/doc_engine/ci/facade_bind_policy.py, tests/ci/test_facade_bind_policy.py, scripts/ci/check_public_surface.py, scripts/ci/check_facade_poke_surface.py, docs/process/session-log.md

## 2026-08-10 — E-LINT0 research: ruff vs ty for top-of-file imports (DeepWiki Ask)
Commit: e153f5c1
Tests: not run (docs-only Spec Draft)
Assumptions affected:
- ruff alone catches “import failures” — [Resolved — premature conflation; L1 unused = ruff F401; L3 unresolved = ty unresolved-import]
- DeepWiki is browse-only — [New info — MCP ask_question at mcp.deepwiki.com + llms.txt]
- session-log monolith OK — [New info — E-LOG0 nest Spec seed in memo 46 §6]
Files touched: docs/research/process/46-lint-import-resolution-ruff-vs-ty-2026-08-10.md, docs/research/README.md, docs/research/quality-backlog.md, docs/process/session-log.md

## 2026-08-10 — Skill: DeepWiki MCP + Bloom Create gate before Implement
Commit: 0c90c7e0
Tests: claims OK (skills/agents/docs); not a code change
Assumptions affected:
- DeepWiki is browse-only cartography — [Resolved — skill documents MCP ask_question + llms.txt]
- Spec Draft memos may jump to Implement from chat memory — [Resolved — bloom_gate through Create required]
Files touched: .cursor/skills/principal-se-research-epic/SKILL.md, .cursor/rules/se-quality-constitution.mdc, docs/research/README.md, docs/research/process/46-*, AGENTS.md, docs/process/session-log.md


## 2026-08-10 — E-MDC0 optimized MDC DevEx (activation algebra)

Commit: 793658cd
Tests: check_repo_claims OK; MDC mode smoke PASS (always=2, globs=4, agent=2, manual=1)
Assumptions affected:
- Agent context / alwaysApply layout — prior "3/3 alwaysApply" stack — [Resolved — redistributed to always≤2 + glob lenses + agent-requested + manual; isomorphism demoted; AGENTS slimmed to pointers]
- `CLAUDE.md` Claude SoT / steering — [Still accurate — CLAUDE.md unchanged; Cursor path scoping now MDC globs only]
Files touched: .cursor/rules/*, .cursor/skills/{principal-se-research-epic,cross-domain-isomorphism}/SKILL.md, AGENTS.md, DOMAIN_MAP.md, docs/research/process/47-*.md, docs/research/quality-backlog.md, docs/research/README.md, docs/process/session-log.md

## 2026-08-10 — E-LOG0 nest session-log with LOC pack + content slugs
Commit: 4dd46784
Tests: 5/5 test_pack_session_log; claims OK
Assumptions affected:
- `docs/process/session-log.md` monolith is fine to keep growing — [Resolved — nested `session-log/`; greedy ≤225 packs; date-first `__slug` names from lead title]
- Month/week calendar splits are enough — [Resolved — refused as size SoT; LOC packer + `.pack-order`]
Files touched: docs/process/session-log/**, scripts/process/pack_session_log*.py, tests/ci/test_pack_session_log.py, CLAUDE.md, docs/research/process/46-*, docs/research/quality-backlog.md

## 2026-08-10 — E-LOG0 MDC glob lens for session-log nest
Commit: 192a244b
Tests: MDC mode smoke (globs include session-log-nest); claims n/a for rules-only
Assumptions affected:
- Session-log conventions live only in README/CLAUDE — [New info — glob rule `session-log-nest.mdc` auto-attaches on nest/packer paths; shards stay `.md`]
Files touched: .cursor/rules/session-log-nest.mdc, docs/process/session-log/README.md

## 2026-08-10 — MDC pack: tooling sections on all project rules
Commit: ae4a8755
Tests: MDC line smoke (each rule ≤80); claims n/a for rules-only
Assumptions affected:
- MDC lenses are policy-only without search/CLI affordances — [Resolved — every `.cursor/rules/*.mdc` now carries path-relevant tooling (ast-grep / rg / venv / pre_pr / DeepWiki) + `@adapters/claude/SEARCH.md` where useful]
Files touched: .cursor/rules/*.mdc

## 2026-08-10 — E-TOOL0 complete toolscape incl. Ruby/Go/Clojure lanes
Commit: uncommitted
Tests: not run (docs Spec Draft); DeepWiki Ask on Charm/Babashka/Ruby families
Assumptions affected:
- Toolscape = LLM/agent only — [Resolved — memo 48 audience matrix: repo gates + developer laptop + agent; Ruby/Go/Clojure as Pilot/pattern not tip kernel]
Files touched: docs/research/process/48-*.md, docs/research/quality-backlog.md, docs/research/README.md, .cursor/rules/{principal-research-gate,cross-domain-isomorphism}.mdc

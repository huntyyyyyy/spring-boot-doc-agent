# Text search allow (ripgrep) — Spec + Implement receipt

**Date:** 2026-08-09  
**Epic:** E-SEARCH0 (narrow)  
**Status:** `spec_gate: APPROVED E-SEARCH0` (operator request 2026-08-09 — lift hard deny)  
**Tip branch:** `cursor/local-ci-gate-fix-61f3` only (no sibling research branch)

## Decision

| Choice | Stance |
| --- | --- |
| Allow `Grep` tool + Bash `rg`/`grep`/`egrep`/`fgrep`/`ripgrep` | **Adopt** |
| Prefer `ast-grep` for structural code citations | **Embody** (soft guidance) |
| Keep `deny_text_search.py` as allow no-op + tokenizer home | **Embody** |
| Keep `NETWORK_EGRESS_DENIES` + `deny_raw_network` | **Embody** (unchanged) |
| Scoped `Bash(ast-grep…)` allow when agents declare Bash | **Embody** (unchanged) |
| Hard-deny text search as citation SoT | **Refuse** (was prior policy) |

## Acceptance (Implement)

1. `deny_text_search.decide({"tool_name":"Grep"})["deny"]` is False; `rg` Bash likewise.
2. `.claude/settings.json` deny list has no `Grep` / `Bash(rg:*)` / `Bash(grep:*)`.
3. `check_repo_claims.TEXT_SEARCH_DENIES == ()`; `FORBIDDEN_AGENT_TOOL == ""`.
4. Network denies still required; `test_bash_without_network_denies_fails` stays red without them.
5. CLAUDE.md / SEARCH.md / CONSTRAINTS §10 / agent prompts describe prefer-not-deny.
6. Tests: `tests/adapters/test_deny_text_search.py`, bridge, check F suites, search methodology.

## Explicit non-goals

- Does not weaken Cover% 98.7, complexipy, LOC, or claims checker.
- Does not authorize raw curl/wget/git-clone.
- Does not make text hits sufficient for `[Evidenced — path:line]` without structural re-verify when the claim is structural.

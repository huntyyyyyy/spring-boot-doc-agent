---
title: E-MD0 Design — closed markdown frontmatter by kind (corpus C)
status: APPROVED FOR IMPLEMENT — user ordered Implement after research
date: '2026-08-10'
epic: E-MD0
category: design
claim_tiers: Evidenced / Confirmed
spec_gate: docs/research/process/49-markdown-frontmatter-metadata-schemas-2026-08-10.md
related:
- docs/research/process/49-markdown-frontmatter-metadata-schemas-2026-08-10.md
- docs/research/process/48-complete-toolscape-agent-repo-developer-2026-08-10.md
- scripts/ci/check_repo_claims.py
- docs/design/ddia-north-star/_build_catalog.py
do_not:
- Grow check_repo_claims.py past sibling imports
- Require bloom_* on DDIA, packs, root SoT, skills
- Use remote HF validate-yaml in CI
approved_decisions:
- corpus_C_kind_schemas
- root_sot_derived_only
- sibling_modules_le_225
- pyyaml_for_nested_sources
last_reviewed: '2026-08-10'
---

# E-MD0 Design Spec

Research SoR: [`process/49-…`](../research/process/49-markdown-frontmatter-metadata-schemas-2026-08-10.md).

## Decisions

1. **Kind map (path → schema)** — not one global FM schema.
2. **Root SoT** (`CLAUDE.md`, `AGENTS.md`, `DOMAIN_MAP.md`, `CONSTRAINTS.md`,
   `README.md`, `CONTRIBUTING.md`, `MATURITY_ASSESSMENT.md`, `STATUS.md`):
   **no YAML frontmatter required**; keep `derived:` blocks. Checker **skips**.
3. **Parse:** PyYAML `safe_load` for nested `sources` (dep already present).
4. **Modules** (each ≤225 LOC):
   - `scripts/ci/md_frontmatter_kinds.py` — kinds, allowlists, deprecated
   - `scripts/ci/md_frontmatter_validate.py` — validate + fix helpers
   - `scripts/ci/check_md_frontmatter.py` — CLI walk / `--fix`
5. **Gate:** hard in `pre_pr` standard+ suites (like claims).
6. **Index:** write `docs/research/_frontmatter_index.yaml` on `--fix` /
   `--write-index` (path, title, status, date, epic, related count).

## Kind → rules

| Kind | Match | Required | Allowlist extras | Hard unknown keys |
| --- | --- | --- | --- | --- |
| `research_memo` | `docs/research/**/*.md` except README/archive/index | title, status, date, claim_tiers, related | epic, bloom_*, sources, do_not, spec_gate, last_reviewed, freshness, superseded_by, aliases, sensors… | yes |
| `design_epic` | `docs/design/*.md` (top-level design memos) | same as research | same + approved_* | yes |
| `ddia_page` | `docs/design/ddia-north-star/**` | id, kind, completeness, last_refined | tags, related, path, epub_anchors, title | yes |
| `steering` | `docs/process/steering-prompts/[0-9][0-9]-*.md` | defer to claims (skip here if no FM beyond status/verify) | status, verify, related, note, category, authored | soft unknown |
| `session_pack` | `docs/process/session-log/**` | skip | — | skip |
| `skill_agent` | `**/.cursor/skills/**/SKILL.md`, `**/agents/*.md`, `adapters/claude/**/*.md` with name | name or title optional | description, tools, related | soft |
| `exempt` | root SoT, README indexes, `_frontmatter_index.yaml` peers | skip | — | skip |

**Bloom rule:** if `bloom_gate == required-through-create` → require
`bloom_mcp` (non-empty list) and `sources` with ≥1 recognized nested key.

**Deprecated:** `claim tiers`→`claim_tiers`, `research date`→`date` — `--fix`
rewrites; without fix, hard fail on research/design.

**related:** list of strings; each repo-relative path must exist (or start with
`http://`/`https://`/`external:`).

**freshness advisory:** if `freshness: tip-bound` and `last_reviewed` /
`date` older than 30 days and status not Superseded/Done → soft warning.

## Implement order

MD0-2 → MD0-3 → MD0-4 → MD0-6 tests → MD0-5 pre_pr wire → MD0-7 normalize →
MD0-8 backlog/README.

## Exit

- `python3 scripts/ci/check_md_frontmatter.py` exit 0 on tip after normalize  
- Tests green under `domain_ci_meta`  
- process/48 still validates; process/49 validates  
- E-COH1 may resume after this tip green slice

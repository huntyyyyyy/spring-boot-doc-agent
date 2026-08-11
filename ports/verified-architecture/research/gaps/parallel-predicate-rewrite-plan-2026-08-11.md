---
title: Parallel predicate-prose rewrite — domain partitions
status: ACTIVE
date: '2026-08-11'
doc_role: gap
related:
  - anti-tautology-predicate-prose-2026-08-11.md
  - ../../.cursor/skills/predicate-prose/SKILL.md
---

# Parallel rewrite plan

**Research steal:** domain-isolated partitions + fan-out/fan-in (MIKA / SPD-RAG /
enterprise multi-agent patterns) — assign **disjoint path sets** so agents cannot
overwrite each other; shared instruction = Skill `predicate-prose` only.

| Partition | Paths | Depth |
| --- | --- | --- |
| A | `docs/adr/`, `docs/c4/`, `docs/standards/` | Full rewrite |
| B | `03-requirements/`, `04-constraints/`, `00-governance/`, `01-vision/`, `02-stakeholders/` | Full |
| C | `nests/`, `12-delivery/`, `08-verification/` | Full |
| D | `07-system-design/` | Full (brief: cut tautology, keep tables) |
| E | root + `docs/DOMAIN_MAP.md` + numbered stub READMEs `05–11` | Full |
| F | `research/` | **Light:** openers + banners only — digests stay evidence; no silent meaning change |

**Skip rewrite:** `docs/requirements/` pointers (already SoT pointers), `.cursor/skills` bodies except cold-start already done.

**Consistency locks (all partitions):** Rust Spec host; Refuse Python; WASM Could;
FREEZE deepen-3; whole words; fewer tokens preferred.

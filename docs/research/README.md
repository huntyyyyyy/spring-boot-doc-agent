# Research SoR — domain map (forced entry)

**Before** weighing frameworks or writing Spec/Implement for design-shaped work,
read this map and open the matching domain memo. Soft skills are not enough;
Cursor look-first hooks inject this path and gate design-shaped writes.

| Domain | Path | Use when |
| --- | --- | --- |
| **Cross-cutting SoT** | [`quality-backlog.md`](quality-backlog.md), [`se-quality-synthesis-2026-08-08.md`](se-quality-synthesis-2026-08-08.md) | Active stream; Embody/Adopt/Refuse merge of foundational segments |
| **findings/** | [`findings/`](findings/) | Stalker ledger entries (STK2) — compact events + gap IDs; not chat dumps |
| **process/** | [`process/`](process/) | SDD, foundational SE, frameworks, dynamics, façade/research hooks, legacy remediation Spec, docs taxonomy, **watch/stalker agents** |
| **coverage-quality/** | [`coverage-quality/`](coverage-quality/) | Oracle vs climb, metrics, adequacy, suite-stalking |
| **ci/** | [`ci/`](ci/) | Workflow modularity, CI UX, CodeQL signals skip |
| **kitchen/** | [`kitchen/`](kitchen/) | Kitchen harness modernization |
| **modularity/** | [`modularity/`](modularity/) | Stage-0 ports, test-suite BCs, tools wave 2, AstGrepBackend split, **tach dependency blueprint**, **DDD repo-structure packet E-REPO0 (21 options · 22 quality · 23 capability backcast)** |
| **stage0/** | [`stage0/`](stage0/) | Covering/absence/recall + claim-symbol ADRs (migrated from `claude/research/`) |
| **archive/** | [`archive/`](archive/) | Superseded WIP, receipts, [`claude-lore/`](archive/claude-lore/) — **not** Spec SoT |

## Rules (DOC1 / DOC10)

1. Domains are **≤2 levels** deep under `docs/research/`.
2. Epic IDs (`E-CM0`, `E-DOC0`, …) in frontmatter are the primary cross-ref — not ordinals.
3. If a domain exceeds ~**12** active memos or needs a third nesting level, **reshape** (merge / synthesis / new top-level domain) — do not deepen.
4. Chat transcripts and raw session lore are **refused** as research SoT.
5. Process logs live under [`docs/process/`](../process/) (session-log, tool-quirks, steering-prompts).

## Look-first (Cursor)

- `beforeSubmitPrompt` injects this map.
- Design-shaped `Write` / `StrReplace` requires a session Read of this file (receipt).
- Cloud agents: do **not** rely on `sessionStart` ([Cursor hooks](https://cursor.com/docs/hooks.md)).

Spec: [`process/18-docs-research-taxonomy-claude-consolidation-2026.md`](process/18-docs-research-taxonomy-claude-consolidation-2026.md).
Skill: `.cursor/skills/principal-se-research-epic/SKILL.md`.

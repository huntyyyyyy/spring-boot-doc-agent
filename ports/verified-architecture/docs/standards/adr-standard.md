---
title: Architecture Decision Record standard (Nygard)
status: ACTIVE
date: '2026-08-10'
last_reviewed: '2026-08-11'
---

# Architecture Decision Record standard

**Format:** Title · Context · Decision · Status · Consequences  
**Location:** `docs/adr/adr-NNNN-slug.md`  
**Rule:** One significant decision per file. Supersede, do not delete.

| Section | Must contain | Fail if |
| --- | --- | --- |
| **Context** | Forces that exist without the choice | Restates the title |
| **Decision** | The choice + bound (path/owner) | Echoes Context or title only |
| **Consequences** | ≥1 **negative** trade-off (Nygard) | Praise-only list |

Status vocabulary: Proposed · Accepted · Deprecated · Superseded (by
Architecture Decision Record-xxxx).

C4 diagrams **must cite** Architecture Decision Record IDs for structural
choices. Without them, diagrams are sketches only.

Load-bearing tool / procurement / protocol choices pair with a filled
**Decision Matrix** (`docs/standards/decision-framework.md`) so usage cases,
code loci, and rejected alternatives are explicit — not assertion-only.
FREEZE: deepen existing matrices only; new matrices without human override =
reject.

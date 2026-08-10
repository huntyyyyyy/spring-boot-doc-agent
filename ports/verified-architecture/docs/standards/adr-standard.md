---
title: Architecture Decision Record standard (Nygard)
status: ACTIVE
date: '2026-08-10'
---

# Architecture Decision Record standard

**Format:** Title · Context · Decision · Status · Consequences  
**Location:** `docs/adr/adr-NNNN-slug.md`  
**Rule:** One significant decision per Architecture Decision Record. Supersede, do not delete.

Status vocabulary: Proposed · Accepted · Deprecated · Superseded (by Architecture Decision Record-xxxx).

C4 diagrams **must cite** Architecture Decision Record IDs for structural choices. Without them, diagrams
are sketches only.

For load-bearing tool / procurement / protocol choices, pair the Architecture Decision Record with a
filled **Decision Matrix** (`docs/standards/decision-framework.md`) so usage
cases, code loci, and rejected alternatives are explicit — not assertion-only.

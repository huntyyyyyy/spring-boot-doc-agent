---
name: paper-digest
description: Digest an arXiv paper by type key, sections, checklist, references walk, then GitHub adopters
---

# Skill: Paper digest

## When

Any Must-spine or Definition of Ready research claim; any “we read paper X.”

## Steps

1. Open `research/method/paper-digest-framework.md`.
2. Fetch Atom metadata: `https://export.arxiv.org/api/query?id_list=<id>`.
3. Fetch HTML if present: `https://arxiv.org/html/<id>` — build section map.
4. Assign **primary_type** from the closed set (theoretical, formal-systems,
   empirical, benchmark, systems-artifact, methodological, analytic,
   literature-survey, systematic-review, position). Mark `[Inferred]` unless
   self-labeled. Reminder: arXiv categories are **not** paper-type keys.
5. Copy `research/method/PAPER_DIGEST_TEMPLATE.md` →
   `research/papers-2026-may-aug/digests/<id>-<slug>.md` and fill all slots.
6. Run the type-appropriate understanding checklist.
7. From References / Related Work, queue up to five algorithmic kin; digest at
   least one follow-on or record why none apply.
8. Fill GitHub anti-bogus table (exact vs adjacent).
9. Only then update Embody/Adopt/Refuse or Definition of Ready evidence links.

## Refuse

- Abstract-only “research complete”
- Using arXiv `cs.AI` as if it meant “empirical”
- Promoting Must without digest file

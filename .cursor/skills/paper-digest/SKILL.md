---
name: paper-digest
description: >-
  Digest an arXiv (or peer) paper by inferred type key, section map, type-specific
  checklist, references walk, then GitHub anti-bogus adopters. Use whenever citing
  a paper for Spec, Must spine, Embody/Adopt/Refuse, or Definition of Ready.
---

# Skill: Paper digest

## When

Any paper used as evidence for design-shaped work, Must claims, or research memos.
Invoked by **principal-se-research-epic** Phase A — do not skip for “obvious” papers.

## Source of Truth

`docs/research/method/paper-digest-framework.md`  
Template: `docs/research/method/PAPER_DIGEST_TEMPLATE.md`  
Digests land in: `docs/research/papers/digests/<arxiv-id>-<slug>.md`  
(Port/greenfield trees may mirror under their `research/**/digests/`.)

## Steps

1. Read the framework (closed type keys + anti-bogus filter).
2. Fetch Atom: `https://export.arxiv.org/api/query?id_list=<id>`.
3. Fetch HTML if present: `https://arxiv.org/html/<id>` — build section map.
4. Assign **primary_type** from the closed set. Mark `[Inferred]` unless
   self-labeled. **arXiv categories are not paper-type keys.**
5. Copy the template into `docs/research/papers/digests/` (or port mirror) and
   fill every slot.
6. Run the type-appropriate understanding checklist.
7. From References / Related Work, queue up to five algorithmic kin; digest at
   least one follow-on or record why none apply.
8. Fill GitHub anti-bogus table — separate **exact** vs **adjacent**.
9. Only then update Embody/Adopt/Refuse or Definition of Ready evidence links.

## Refuse

- Abstract-only “research complete”
- Using `cs.AI` / `cs.SE` as if it meant empirical / theoretical
- Promoting Must Adopt when only adjacent repos exist
- Treating Zenodo study zips or unreleased org profiles as shipped products

---
name: fill-wave-gap
description: Close a blocks_code open question or write a six-part QAS without slipping into product code
---

# Skill: Fill wave gap

## When to use

Working an item from `STATUS.md` or an `OQ-*.md` with `blocks_code: true`.

## Steps

1. Open the OQ or QAS target file; quote the question.
2. Prefer writing the answer under the matching `00/`–`12/` folder
   (not only chatting).
3. If NFR-related: use `03-requirements/qas/TEMPLATE.md` six-part form.
   Incomplete measure ⇒ demote from Must / mark Spike — do not invent Design.
4. Keep constraints in `04-constraints/`; do not smuggle them into REQs.
5. Cite research paths with claim tiers; do not paste whole memos.
6. Update OQ `status:` to `SPIKE` | `CLOSED` | `WAIVED`.
7. Update `STATUS.md` and DoR row if a predicate moved.
8. **Refuse** creating product language trees as “help.”

## Exit

Diff touches planning Markdown only; STATUS reflects the new truth.

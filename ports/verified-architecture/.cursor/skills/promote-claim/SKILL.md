---
name: promote-claim
description: Promote a research claim into authoritative docs/ with claim-tier honesty
---

# Skill: Promote claim

## When to use

A finding in `research/` should become product Source of Truth under `docs/`.

## Steps

1. Quote the claim and its tier (Evidenced / Confirmed / Unknown).
2. Refuse promotion of Unknown without marking MEASURE-TBD or Spike.
3. Choose destination: `docs/requirements/`, `docs/constraints/`,
   `docs/adr/`, `docs/c4/`, or `docs/standards/`.
4. Keep IDs stable; link back to the research path in a short “Evidence” note.
5. Do not delete the research memo — corpus stays for Retrieval-Augmented Generation.
6. Update `docs/DOMAIN_MAP.md` only if a new navigational entry is required.

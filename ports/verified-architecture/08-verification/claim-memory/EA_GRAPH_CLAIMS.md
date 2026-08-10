---
title: EA-Graph claim memory — Spec (adopt 2608.04278)
status: DRAFT
date: '2026-08-10'
arxiv: '2608.04278'
---

# EA-Graph claim memory (product Spec)

We **Adopt** the paper’s model for *verification claims*, not its synthetic
benchmark worlds as plants.

## Objects

| Object | Meaning |
| --- | --- |
| Artifact node | Sub-path (file or finer) with content digest |
| Claim | “Lock L holds / resolve R = bean B / cycle absent” at time T |
| Anchor | Binding claim → artifact identity + digest used when established |
| Meta | Independent `(evidence_strength, freshness)` |
| Disposition | `unaffected` \| `affected` \| `unprovable` after withdrawal query |

## Withdrawal algorithm (Spec)

```text
for each stored claim C:
  recompute digests of ANCH(C)
  if digests unchanged → disposition = unaffected
  else if replacement content available → mark affected; require re-verify
  else → disposition = unprovable   # DO NOT GUESS
```

## Storage (design)

- Table/collection `claims` beside registry (same SQLite file OK in MVP).
- Not agent conversational memory (`AgentMemory` port stays separate).
- Rebuildable from receipts + current files; git does **not** sync claim DB blobs
  as team SoR (locks in git remain policy SoR).

## API sketch (ICD later)

- `claim_put(claim, anchors[])`
- `claim_withdraw(repo_snapshot) -> dispositions[]`
- `claim_get(claim_id)`

## Accept (W1)

Fixture: establish claim on file A; edit A; withdraw → `affected` or
`unprovable`; never invents a new resolve edge.

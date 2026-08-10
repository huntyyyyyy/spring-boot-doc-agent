---
title: Artifact-anchored claim memory — specification (adopt 2608.04278)
status: DRAFT
date: '2026-08-10'
arxiv: '2608.04278'
paper_title: 'EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift'
---

# Artifact-anchored claim memory (product specification)

We **Adopt** the paper *EA-Graph: Artifact-Anchored Verification Memory for
Coding Agents under Upstream Drift* for *verification claims*, not its
synthetic benchmark worlds as plants.

Whole words in prose — see root `GLOSSARY.md`.

## Objects

| Object | Meaning |
| --- | --- |
| Artifact node | Sub-path (file or finer) with content digest |
| Claim | “Lock L holds / resolve R = bean B / cycle absent” at time T |
| Anchor | Binding claim → artifact identity + digest used when established |
| Meta | Independent `(evidence_strength, freshness)` |
| Disposition | `unaffected` \| `affected` \| `unprovable` after withdrawal query |

## Withdrawal algorithm (specification)

```text
for each stored claim C:
  recompute digests of ANCH(C)
  if digests unchanged → disposition = unaffected
  else if replacement content available → mark affected; require re-verify
  else → disposition = unprovable   # DO NOT GUESS
```

## Storage (design)

- Table/collection `claims` beside registry (same SQLite file OK in minimum viable product).
- Not agent conversational memory (`AgentMemory` port stays separate).
- Rebuildable from receipts + current files; git does **not** sync claim database blobs
  as team System of Record (locks in git remain policy System of Record).

## Application programming interface sketch (Interface Control Document later)

See `07-system-design/icd/ea-graph-claims.schema.json` and
`receipts/receipt-schema-draft.md`.

---
title: Artifact-anchored claim memory — specification (Pilot invent from 2608.04278)
status: DRAFT — Pilot; exact public engines = 0
date: '2026-08-10'
arxiv: '2608.04278'
paper_title: 'EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift'
---

# Artifact-anchored claim memory (product specification)

**Embody** `unprovable`, evidence≠freshness, leaf anchors from EA-Graph
(2608.04278). **Refuse** industry-Adopt of a field library (public engines =
0). Stance: **Pilot invent** under Spike before Must Implement.

Whole words — root `GLOSSARY.md`.

## Objects

| Object | Attribute (not in name) |
| --- | --- |
| Artifact node | Sub-path + content digest |
| Claim | Lock/resolve/cycle assertion at time T |
| Anchor | Claim → artifact identity + establishing digest |
| Meta | Independent `(evidence_strength, freshness)` |
| Disposition | `unaffected` \| `affected` \| `unprovable` after withdrawal |

## Withdrawal (fail closed)

```text
for each stored claim C:
  recompute digests of ANCH(C)
  if digests unchanged → unaffected
  else if replacement content available → affected; require re-verify
  else → unprovable   # DO NOT GUESS
```

Guessed bean/edge on `unprovable` → reject.

## Storage

- `claims` beside registry (same SQLite OK in MVP).
- Not `AgentMemory` conversational port.
- Rebuildable from receipts + files; git does **not** sync claim DB as team SoR
  (locks in git remain policy SoR).

## ICD later

`07-system-design/icd/ea-graph-claims.schema.json` ·
`receipts/receipt-schema-draft.md`.

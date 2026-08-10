---
title: Ubiquitous language — Unknown / unprovable
status: DRAFT
date: '2026-08-10'
---

# Unknown taxonomy (draft)

| Code | Meaning | Agent/human action |
| --- | --- | --- |
| `MULTI_IMPL` | Multiple beans match; no qualifier/primary | Do not pick; show candidates |
| `MISSING_BEAN` | Type requested; none registered | Fail lock or report gap |
| `STALE_INDEX` | Index digest ≠ sources | Rebuild index; don’t verify cold |
| `UNSUPPORTED_DI` | Outside static envelope (profiles/AOP/…) | Unknown — not “ok” |
| `STALE_ANCHOR` | Claim evidence content changed (EA-Graph) | Re-verify or mark affected |
| `UNPROVABLE` | Needed witness content unavailable | **Do not guess** |

**Rule:** `UNPROVABLE` and `MULTI_IMPL` never coerce into a concrete edge.

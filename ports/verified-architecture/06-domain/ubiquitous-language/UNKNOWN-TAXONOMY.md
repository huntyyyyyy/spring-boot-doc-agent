---
title: Ubiquitous language — Unknown / unprovable
status: DRAFT
date: '2026-08-10'
---

# Unknown taxonomy (draft)

Disposition codes for resolve / claim memory. Coercion into a concrete edge
when code is `UNPROVABLE` or `MULTI_IMPL` → reject.

| Code | Attribute | Required action |
| --- | --- | --- |
| `MULTI_IMPL` | Multiple beans match; no qualifier/primary | Show candidates; do not pick |
| `MISSING_BEAN` | Type requested; none registered | Fail lock or report gap |
| `STALE_INDEX` | Index digest ≠ sources | Rebuild; do not verify cold |
| `UNSUPPORTED_DI` | Outside static envelope (profiles/AOP/…) | Unknown — not “ok” |
| `STALE_ANCHOR` | Claim evidence content changed | Re-verify or mark affected |
| `UNPROVABLE` | Needed witness unavailable | **Do not guess** |

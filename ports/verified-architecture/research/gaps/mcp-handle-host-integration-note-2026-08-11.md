---
title: Host integration note — Model Context Protocol handles (stdio MVP)
status: DRAFT — Hypothesis
date: '2026-08-11'
freeze_class: deepen-3
related:
  - research/gaps/deepen-mcp-handle-lifecycle-2026-08-11.md
  - 07-system-design/icd/mcp-tools.md
accepted: false
---

# Host integration note — handles (stdio MVP)

If the presentation host speaks Model Context Protocol over local stdio with no
remote principal, **then** possession of a harness-minted handle is treated as
capability for that process: the model may pass `snapshot_id` only if a prior
tool result returned it.

If the same product later exposes Streamable HTTP with auth, **then** possession
must not equal authorization: SEP-2567 Security separates those
`[Evidenced — mcp-open-items]`. Do not design stdio MVP as if remote auth were
already solved.

If two agents share one engine without per-agent handle tables, **then** a
stolen or guessed `snap_` string is a cross-agent confused-deputy risk — mitigate
by unguessable mint entropy and short expiry, not by trusting the prefix alone
`[Hypothesis — unmeasured]`.

This note is **not** an Accept of TTL=1h and **not** Implement guidance for crates.

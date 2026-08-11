---
title: Deepen-3 — Model Context Protocol handle lifecycle
status: RESEARCH — Hypothesis only
date: '2026-08-11'
freeze_class: deepen-3
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - research/papers-2026-may-aug/digests/2608.03609-stead-agentic-verification.md
  - research/gaps/mcp-open-items-research-2026-08-10.md
  - 07-system-design/icd/mcp/common.schema.json
  - 08-verification/stead/STEAD_CONSTRAINTS.md
implements: FREEZE deepen row — handle lifecycle only
accepted: false
---

# Deepen-3: handle lifecycle (not Adopt)

If the wire dialect is already pinned (`2026-07-28`) and our tool *names*
remain Pilot invent, then the next falsifiable work is how handles are minted,
bound, expired, and rejected — not a new tool list and not an FO checker.

This memo deepens that row. Every product rule below is a **Hypothesis** until
a Spike measures it or a human Accepts an Interface Control Document amendment.
No Architecture Decision Record rewrite. No parallel schema files.

Whole words — root `GLOSSARY.md`.

---

## What the sources actually constrain

**If** Model Context Protocol SEP-2567 removes sessions, **then** application
state must travel as tool arguments (opaque ids), not as `Mcp-Session-Id`
`[Evidenced — mcp-open-items; blog 2026-07-28]`.

**If** a handle is only a tool-design pattern (not a wire type), **then** mint,
durability, and expiry errors are *our* harness obligations — the Spec will not
ship a standard `Handle` object for us to Adopt
`[Evidenced — SEP-2567 via open-items]`.

**If** arXiv 2608.03609 never mentions Model Context Protocol handles, mint,
snapshot digests, or TTL (digest §8), **then** STEAD cannot validate our
`snap_` / `expires_at` design. What it *does* justify Embodying: free-text
entity ids and Offer-outside calls are the failure mode ST-1/ST-5 already name;
unrestricted FO verification over agent+tools+data is undecidable, so ST-3
refuses “agent satisfies business FO” without a Spike
`[Evidenced — digest 2608.03609]`.

**If** public equivariance-wrapper engines remain 0, **then** ST-2 stays Spike /
Hypothesis — not a shipped wrap Adopt
`[Confirmed — digest; STEAD_CONSTRAINTS]`.

---

## Lifecycle as four predicates (product Hypothesis)

Schemas already encode prefixes and `expired_handle`
(`icd/mcp/common.schema.json`, `snapshot_open.output`). Semantics that still
lack a plant:

| Step | Predicate (Hypothesis) | Fail → reject_class |
| --- | --- | --- |
| **Mint** | Only `snapshot_open` (and later catalog tools) may allocate a `snap_` / `lock_` / … string; the model never invents one | `unknown_handle` |
| **Bind** | Mint response records `tree_sha` + `index_sha` (+ optional `registry_epoch`); later tools that require `snapshot_id` re-check those digests against the live tree/index | `digest_mismatch` / `index_stale` |
| **Expire** | Handle dies when `now ≥ expires_at` **or** when bound digests no longer match — whichever first; no silent refresh of the same id | `expired_handle` |
| **Use** | `resolve` / `claim_withdraw` require a live `snapshot_id`; `verify` / `locks_list` may omit it but then forfeit digest pinning | `unknown_handle` / `binding_incomplete` |

**If** expiry is wall-clock only, **then** a long-lived agent can keep a
`snap_` whose tree has moved underneath it unless digest re-check also runs.
Open-items already pairs TTL with digest drift; that pairing is the Hypothesis
to Spike — not “1 hour” as a sacred number
`[Evidenced — open-items §2; Unknown — measured TTL]`.

**If** refresh means “call `snapshot_open` again,” **then** the old id must
fail closed. Silent upgrade of `snap_old` → new digests would hide which view
`resolve` used.

---

## What STEAD does *not* buy us

| Temptation | Why it fails |
| --- | --- |
| Cite 2608.03609 as proof of handle TTL | Paper silent on handles |
| Ship FO-CTL checker to “close” handle research | Wrong plant; PSPACE checker Refuse for MVP |
| Treat ST-5 as theorem about Model Context Protocol | ST-5 is Embody invention aligned with Offer discipline, not a paper theorem |
| Add tools to “complete” the lifecycle | FREEZE: stop adding tools; deepen semantics of the five primitives |

---

## Sequencing note

The honesty audit listed deepen order β/ρ → withdrawal → handles. This pass
takes **handles first** because: if the wire pin is the only true Adopt on the
spine, then handle mint/bind/expire is where Spec evidence can still constrain
invention before receipt algebra invents a second freshness story. β/ρ remains
FREEZE-allowed and next.

---

## Decidable “deepen done” for this vector

Mark this deepen row **complete** only when all of:

1. Digest **2608.03609** present with type + section map + handle-silence table
   (this commit satisfies the digest half).
2. One **host-integration note** stating: stdio MVP treats possession of a
   minted handle as capability; remote auth later must not equate possession
   with authorization `[Evidenced — SEP-2567 Security via open-items]` —
   **Present** as Draft: `mcp-handle-host-integration-note-2026-08-11.md`
   (not yet an Interface Control Document amendment Accept).
3. A Spike charter exit that **measures** expiry: either wall-clock plant or
   explicit “Pilot invent, unmeasured TTL” recorded next to `expires_at` — not
   a Chosen score. Charter stub: `12-delivery/spike-charters/SPIKE-handle-TTL.md`
   (unmeasured until Spike runs).
4. Language demotion: no “Chosen 12/12” / “STEAD normative” left on the handle
   path (open-items alternatives table already says Working hypothesis; keep it).

Until (3) measures or records Pilot-invent TTL and (4) residuals are gone,
status stays **RESEARCH — Hypothesis**. Definition of Ready D0 does **not**
flip to PASS from this memo alone (β/ρ Fresh Spike and withdrawal charter
still open).

---

## Allowed follow-ups (still not Implement)

- Line-level Interface Control Document amendment *proposals* (human review):
  document digest-or-TTL expire rule next to `snapshot_open`; do not fork schemas.
- Spike: rename-id attack examples for ST-2 (`SPIKE-STEAD-equivariance`) — keep/drop
  wrap; no product code.
- Next deepen vector: receipt β/ρ + digest **2607.14890**.

## Forbidden follow-ups

- Parallel `docs/design/ir/*` or nest `schema.sql` “Ready” files.
- New tools or Decision Matrices.
- Claiming Implement-Ready or DoR PASS from handle prose.

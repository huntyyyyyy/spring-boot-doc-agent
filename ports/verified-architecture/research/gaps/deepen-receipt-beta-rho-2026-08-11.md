---
title: Deepen-1 — Receipt β/ρ vs receipt.schema.json
status: RESEARCH — Hypothesis / Pilot
date: '2026-08-11'
freeze_class: deepen-3
claim_tiers: Evidenced / Confirmed / Unknown
look_first:
  - research/papers-2026-may-aug/digests/2607.14890-proof-or-stop.md
  - 07-system-design/icd/receipt.schema.json
  - 08-verification/receipts/receipt-schema-draft.md
  - 12-delivery/spike-charters/SPIKE-receipt-fresh.md
implements: FREEZE deepen row — receipt freshness β/ρ
accepted: false
---

# Deepen-1: β/ρ onto product receipt SoT (no crates)

**If** digests and schemas already exist, **then** deepen means mapping paper
symbols onto `icd/receipt.schema.json` and chartering Spikes — not a second
schema SoT and not Implement.

Single receipt System of Record: `07-system-design/icd/receipt.schema.json`.  
`08-verification/receipts/receipt-schema-draft.md` is a **pointer only**.

Whole words — root `GLOSSARY.md`. Digest: `2607.14890-proof-or-stop.md` §8.

---

## Map (Embody / Pilot)

| Paper (Proof-or-Stop) | Product field | Tier |
| --- | --- | --- |
| \(\mathsf{headHash}\) | `head_hash` (required) | Embody |
| \(\mathsf{materialHash}\) | `material_digest` (required) | Embody — ls-tree exclusion list still Spike |
| \(\mathsf{policyHash}\) | `policy_digest` (required) | Embody — canon serialization Unknown |
| \(\mathsf{commandSetHash}\) | `command_set_digest` (required) | Embody — set serialization Unknown |
| \(\mathsf{storyFilesHash}\) | **Absent** as required | **Pilot** — add only after Accept, or keep outside MVP |
| \(\rho(E)\) command tuple | `steps[]` when `kind=command` (`cmd`, `args`, `cwd`, `exit`, `output_digest`) | Embody |
| \(\mathrm{Fresh}\) | Not a named schema predicate | Spike / Pilot invent — see `SPIKE-receipt-fresh.md` |
| Signatures / ProducerAuthorized | Not in MVP required set | Hypothesis — unsigned minimum |

Public Proof-or-Stop product engines = **0** → **Refuse** Must Adopt of their
engine; keep Embody field shapes.

---

## Decidable deepen done

1. Digest **2607.14890** Present with β/ρ § map — **done**.  
2. Dual SoT demoted (draft → pointer; VERIFY_STACK → ICD) — **done**.  
3. Spike charter for Fresh / ls-tree exclusion **or** explicit “Pilot invent,
   Fresh unmeasured” — see `SPIKE-receipt-fresh.md`.  
4. Human Accept of schema still **pending** (Definition of Ready D10 PARTIAL).

No crates. No parallel `docs/design/ir/` receipt forks.

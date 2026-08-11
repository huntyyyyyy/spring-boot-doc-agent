---
title: Receipt schema draft — POINTER only
status: SUPERSEDED AS SoT — 2026-08-11
date: '2026-08-10'
traces: open question OQ-05
---

# Receipt / proof-tour — do not edit this as System of Record

**Interface Control Document System of Record:**  
`07-system-design/icd/receipt.schema.json`

That schema requires `head_hash`, `material_digest`, `policy_digest`,
`command_set_digest`, and ρ fields on `steps[]` when `kind=command`.

This file remains only as a historical proof-tour sketch. Editing it does
**not** change the contract. Fail-mode: dual SoT (draft vs ICD) → agents
implement the weak shape.

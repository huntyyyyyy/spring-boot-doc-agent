---
title: Definition of Ready — wave before AI product codegen
status: ACTIVE
---

# Definition of Ready (DoR)

Implement Ready = all PASS or WAIVED with signoff.  
**Port Ready** is separate — see `PORT_READY.md`.

| # | Predicate | Evidence | Status |
| --- | --- | --- | --- |
| D1 | Product boundary draft present | `01-vision/.../BOUNDARY.md` | PARTIAL (Awaiting human Accept) |
| D2 | Wave Must StRS/SRS named | `03-requirements/strs|srs` | PARTIAL (Draft present) |
| D3 | Must NFRs as six-part QAS | `03-requirements/qas/` | PARTIAL (N-05..08 complete; N-01/02 Spike-blocked) |
| D4 | Constraints ledger | `04-constraints/technical/constraints-wave1.md` | PARTIAL (Draft) |
| D5 | blocks_code OQs closed/waived | `open-questions/` | FAIL (awaiting Accept) |
| D6 | SoR matrix Draft | `sor-derived-matrix.md` | PARTIAL |
| D7 | Ports + ICD stubs | `PORTS.md`, `icd/*` | PARTIAL (schemas drafted) |
| D8 | C4 Context+Container | legacy `docs/c4/` | PARTIAL |
| D9 | ADRs / brief | `ARCHITECTURE_BRIEF.md` | PARTIAL |
| D10 | Receipt schema | `icd/receipt.schema.json` | PARTIAL |
| D10b | EA-Graph claim Spec+schema | `claim-memory/`, `ea-graph-claims.schema.json` | PARTIAL |
| D10c | STEAD in MCP ICD | `stead/`, `mcp-tools.md` | PARTIAL |
| D11 | V&V Accept methods | `vv-plan/` | PARTIAL (fixtures named) |
| D12 | Human wave Approve | `signoff/SIGNOFF_LOG.md` | FAIL |

**Port Ready:** `PORT_READY.md` checklist PASS — export Spec corpus now.  
**Implement:** still Refuse.

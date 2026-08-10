---
title: Definition of Ready — wave before AI product codegen
status: ACTIVE
---

# Definition of Ready (DoR)

A wave is **Ready for Spike/Implement** only when all rows are `PASS` or
explicitly `WAIVED` with human sign-off in `02-stakeholders/signoff/`.

| # | Predicate | Evidence path | Status |
| --- | --- | --- | --- |
| D1 | Product boundary one-liner Accepted | `01-vision/problem-frame/BOUNDARY.md` | PARTIAL (draft; human Accept open) |
| D2 | Wave Must StRS/SRS set named | `03-requirements/` | FAIL |
| D3 | Every Must NFR has complete six-part QAS | `03-requirements/qas/` | FAIL |
| D4 | Constraints ledger current | `04-constraints/` + legacy `docs/constraints/` | PARTIAL |
| D5 | No open `blocks_code` OQs (or WAIVED) | `04-constraints/open-questions/` | FAIL |
| D6 | SoR vs derived matrix Draft Accepted | `08-verification/sor-derived-matrix.md` | PARTIAL (draft) |
| D7 | Ports + ICD stubs for spike seam | `ports-and-adapters/PORTS.md`, `icd/` | PARTIAL (schemas still missing) |
| D8 | C4 Context + Container cite ADRs | `07-system-design/c4/` or legacy `docs/c4/` | PARTIAL |
| D9 | Irreversible choices have Accepted ADRs; else options/ | `ARCHITECTURE_BRIEF.md` + adr/ | PARTIAL |
| D10 | Receipt / proof-tour schema named | `08-verification/receipts/receipt-schema-draft.md` | PARTIAL (draft) |
| D11 | V&V / fixture Accept methods named | `08-verification/vv-plan/` | FAIL |
| D12 | Human wave Approve recorded | `02-stakeholders/signoff/` | FAIL |

**Agent rule:** if any row is `FAIL` or `PARTIAL` awaiting Accept, refuse product
codegen; work the next item in `STATUS.md` instead.

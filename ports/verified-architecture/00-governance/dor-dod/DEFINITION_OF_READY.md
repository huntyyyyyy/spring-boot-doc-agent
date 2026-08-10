---
title: Definition of Ready — wave before AI product codegen
status: ACTIVE
---

# Definition of Ready (DoR)

A wave is **Ready for Spike/Implement** only when all rows are `PASS` or
explicitly `WAIVED` with human sign-off in `02-stakeholders/signoff/`.

| # | Predicate | Evidence path | Status |
| --- | --- | --- | --- |
| D1 | Product boundary one-liner Accepted | `01-vision/problem-frame/` | FAIL |
| D2 | Wave Must StRS/SRS set named | `03-requirements/` | FAIL |
| D3 | Every Must NFR has complete six-part QAS | `03-requirements/qas/` | FAIL |
| D4 | Constraints ledger current | `04-constraints/` + legacy `docs/constraints/` | PARTIAL |
| D5 | No open `blocks_code` OQs (or WAIVED) | `04-constraints/open-questions/` | FAIL |
| D6 | SoR vs derived matrix Draft Accepted | `08-verification/` | FAIL |
| D7 | Ports + ICD stubs for spike seam | `07-system-design/ports-and-adapters/`, `icd/` | FAIL |
| D8 | C4 Context + Container cite ADRs | `07-system-design/c4/` or legacy `docs/c4/` | PARTIAL |
| D9 | Irreversible choices have Accepted ADRs; else options/ | `07-system-design/adr/` | PARTIAL |
| D10 | Receipt / proof-tour schema named | `08-verification/receipts/` | FAIL |
| D11 | V&V / fixture Accept methods named | `08-verification/vv-plan/` | FAIL |
| D12 | Human wave Approve recorded | `02-stakeholders/signoff/` | FAIL |

**Agent rule:** if any row is `FAIL`, refuse product codegen; work the
next FAIL in `STATUS.md` order instead.

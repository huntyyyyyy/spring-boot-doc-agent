# No-code gate

**Fail closed:** any AI product codegen while any row below is red.

Mirror of root `CONTRIBUTING.md` + BFS Definition of Ready:

| # | Predicate (must hold) | Fail-mode if violated |
| --- | --- | --- |
| 1 | Wave Must REQs Accepted (or explicit Draft-wave Approve) | codegen blocked |
| 2 | No open `blocks_code: true` without WAIVED | codegen blocked |
| 3 | Must NFRs are complete six-part Quality Attribute Scenario | codegen blocked |
| 4 | Constraints ledger current | codegen blocked |
| 5 | C4 Context+Container; Component only for touched BC | codegen blocked |
| 6 | Relevant ADRs Accepted; options/ holds the rest | codegen blocked |
| 7 | Ports + ICD stubs for the spike seam | codegen blocked |
| 8 | Receipt / V&V schema named | codegen blocked |

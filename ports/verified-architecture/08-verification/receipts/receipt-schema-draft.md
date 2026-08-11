---
title: Receipt schema draft (proof tour v0)
status: DRAFT
date: '2026-08-10'
traces: open question OQ-05
---

# Receipt / proof-tour (v0)

JSON object per `verify` run. Fields mandatory unless marked optional.

```json
{
  "receipt_version": "0.1.0",
  "run_id": "uuid-v4",
  "git_commit": "40-hex or dirty workspace marker",
  "target_root": "path",
  "result": "pass|fail|unknown",
  "steps": [
    {
      "step_id": "STEP-0001",
      "kind": "index_load|annotation|resolve|lock_check|policy",
      "rule_id": "optional RULE-…",
      "lock_id": "optional",
      "witness": {
        "file": "rel/path",
        "line": 1,
        "column": 0,
        "symbol": "optional scip symbol",
        "edge_id": "optional registry edge"
      },
      "message": "human readable",
      "ok": true
    }
  ],
  "unknowns": [
    {
      "code": "MULTI_IMPL|MISSING_BEAN|STALE_INDEX|UNSUPPORTED_DI|UNPROVABLE|STALE_ANCHOR",
      "detail": "string",
      "evidence_ok": true,
      "freshness": "fresh|stale|unknown"
    }
  ],
  "claim_dispositions": [
    {
      "claim_id": "optional",
      "disposition": "unaffected|affected|unprovable",
      "anchor_digest": "content digest used when claim was established"
    }
  ]
}
```

## Invariants (fail closed)

| # | Predicate | Fail-mode |
| --- | --- | --- |
| 1 | Fail run has non-empty `steps` | Empty `steps` → invalid receipt |
| 2 | `witness` excludes LLM/RAG strings | Present → invalid |
| 3 | Evidence ⊥ freshness | Silent guess on stale anchor → reject |
| 4 | Prefer `unprovable` over inventing bean/edge | Invented edge → reject |
| 5 | `step_id` stable when inputs unchanged | *(Unknown until Spike defines key)* |

Jul–Aug amendment: `research/adversarial/july-august-2026-overturn-review.md` §4 A1.

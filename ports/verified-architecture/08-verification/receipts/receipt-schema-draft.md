---
title: Receipt schema draft (proof tour v0)
status: DRAFT
date: '2026-08-10'
traces: OQ-05
---

# Receipt / proof-tour (v0)

JSON object per `verify` run. All fields mandatory unless marked optional.

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
      "code": "MULTI_IMPL|MISSING_BEAN|STALE_INDEX|UNSUPPORTED_DI",
      "detail": "string"
    }
  ]
}
```

## Invariants

1. Fail with empty `steps` is invalid.
2. LLM/RAG strings must not appear inside `witness`.
3. `step_id` stable for the same logical check across runs when inputs unchanged *(Unknown until Spike defines stability key)*.

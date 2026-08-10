---
title: Tactics and ATAM tradeoff points
status: DRAFT
date: '2026-08-10'
---

# Tactics · sensitivity · tradeoffs

| Decision knob | Helps | Hurts | Class |
| --- | --- | --- | --- |
| Aggressive SCIP/registry cache | Latency QAS | Freshness / stale false-green | Tradeoff |
| WASM LockCheck guest | Isolation | Latency; drift vs native | Tradeoff |
| SQLite registry | Deterministic verify | Recursive query UX | Sensitivity |
| EDN + Clojure brain | Query richness | Dual-view drift | Tradeoff |
| Go async watch | Perceived freshness | Consistency windows | Tradeoff |
| Unknown hard-fail | Safety | “Green” availability | Tradeoff |
| RAG on verify path | Suggest UX | Truthfulness | **Refuse for Must** |

Record chosen tactics in ADRs — not only in this table.

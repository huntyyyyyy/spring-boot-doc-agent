---
title: Tactics and Architecture Tradeoff Analysis Method tradeoff points
status: DRAFT
date: '2026-08-10'
---

# Tactics · sensitivity · tradeoffs

**Historical / evidence — not product SoT.** Knob catalog — chosen tactics land
in Architecture Decision Records, not only here. Fail-mode: Retrieval-Augmented
Generation on the verify path as Must.

| Decision knob | Helps | Hurts | Class |
| --- | --- | --- | --- |
| Aggressive Source Code Index Protocol/registry cache | Latency Quality Attribute Scenario | Freshness / stale false-green | Tradeoff |
| WebAssembly LockCheck guest | Isolation | Latency; drift vs native | Tradeoff |
| SQLite registry | Deterministic verify | Recursive query UX | Sensitivity |
| EDN + Clojure brain | Query richness | Dual-view drift | Tradeoff |
| Go async watch | Perceived freshness | Consistency windows | Tradeoff |
| Unknown hard-fail | Safety | “Green” availability | Tradeoff |
| Retrieval-Augmented Generation on verify path | Suggest UX | Truthfulness | **Refuse for Must** |

Record chosen tactics in Architecture Decision Records — not only in this table.

---
title: E-CX0 — Code intelligence program (stage specs)
status: DRAFT Spec — parked; not Approve; not Active tip; no Implement
research date: 2026-08-13
spec_gate: DRAFT E-CX0 (2026-08-13)
bloom_gate: required-through-create
bloom_mcp:
  - deepwiki_cartography  # session catalog had no DeepWiki MCP; pages fetched
  - llms_txt
claim tiers: Evidenced / Confirmed / Unknown
product: operator adopt + scanning BC slice; not a write kernel
related:
  - docs/design/code-intel/s0-serena-adopt.md
  - docs/design/code-intel/s0-operator-runbook.md
  - docs/design/code-intel/s0-ocs-run-log-2026-08-13.md
  - docs/design/code-intel/s1-resolved-facts.md
  - docs/design/code-intel/s2-verify-loop.md
  - docs/research/quality-backlog.md
  - docs/research/process/50-intent-kernel-v3-consolidated-2026-08-13.md
  - docs/design/intent-kernel-cas-apply-design-2026-08-13.md
  - CONSTRAINTS.md
  - spring-signals/docs/CAMPAIGN.md
do_not:
  - implement product code on this tip (#119 / E-COH1 stays Active)
  - start S1 before S0 go/no-go and human Approve
  - build indices, SPO graphs, planners, or cas-apply
  - treat tags as model trust without S2 ablation
  - nest writes under doc_engine
sources:
  primary:
    - https://github.com/oraios/serena
    - https://oraios.github.io/serena/01-about/035_tools.html
    - https://oraios.github.io/serena/01-about/020_programming-languages.html
    - https://ast-grep.github.io/llms.txt
  deepwiki:
    - https://deepwiki.com/oraios/serena
---

# E-CX0 — Code intelligence (implementation specs)

**Not Approve. Not Active.** These files are the implementable split of the
code-intelligence verdict. Kernel C4 (`intent-kernel-cas-apply-design-2026-08-13.md`)
is **historical / deferred**, not this program.

**Two product homes (do not collapse):**

| What | Home | Decision |
| --- | --- | --- |
| Serena, resolved Spring facts, verify-loop | **This repo** (E-CX0; scanning BC + operator) | Not a new repo. |
| CAS + deny + receipt write kernel | **Greenfield** `intent-kernel` (E-IK0) | D-00 = **B**, D-01 = **(b)** locked 2026-08-13. Deferred as program. |

OpenRewrite + git + a small deny check stay the write path until that path
loses a **named** mutation class. Do not nest writes under `doc_engine`.

```text
Iso: observe → act → remeasure ≅ agent invokes a checker | I3: units
(pass-rate vs fail_under) | I5: no oracle-floor retype
```

## 0. Sequence (one stage at a time)

| Stage | Spec | Deliverable | Product code? |
| --- | --- | --- | --- |
| **S0** | [s0-serena-adopt.md](s0-serena-adopt.md) + [s0-operator-runbook.md](s0-operator-runbook.md) + [s0-ocs-run-log-2026-08-13.md](s0-ocs-run-log-2026-08-13.md) | Pin Serena + jdtls; freeze 12 questions; run on `ocs-api-service` | **No** |
| **S1** | [s1-resolved-facts.md](s1-resolved-facts.md) | CLI extractor: resolved annotations / mappings / wiring as `facts.jsonl` | Yes, after Approve **and** S0 miss |
| **S2** | [s2-verify-loop.md](s2-verify-loop.md) | Agent **runs** existing verifiers; cite `file:line` | Skill/prompt; no new index |

Stop rules are **in the stage spec**. If S0’s LSP answers the frozen Spring
questions, **do not build S1**. If S2’s A/B misses the pass-rate delta,
**abandon** the extra loop — do not add a warehouse.

Active tip remains land **#119** then **E-COH1**. S1 Implement is a later
tip, after those and after human Approve of this epic.

## 1. Ranking (why this split)

| Rank | Approach | Landing |
| --- | --- | --- |
| 1 | Verification-in-the-loop | **S2** |
| 2 | Spring-resolved fact extractor in this repo | **S1** |
| 3 | Adopt Serena / jdtls + grep | **S0** |
| 4 | Writes: OpenRewrite + git + deny | **Cut** (not these specs) |
| 5 | Custom index | **Cut** until 1–3 lose |
| 6 | cas-apply Intent Kernel | **Defer indefinitely** (E-IK0) |

## 2. Where the chat tools actually landed

| Proposed in other chats | Landing |
| --- | --- |
| Serena / jdtls / MCP navigation | **S0 Adopt** — not a repo we write |
| Spring-resolved extractor, CodeQL pack, facts.jsonl | **S1** — this repo, after a named S0 miss |
| Agent runs CodeQL / ArchUnit / `pipeline gates` | **S2** |
| OpenRewrite + git | Rank 4 write path — **cut** from this epic |
| Fact Store, SPO graph, semantic index, planner | **Cut** |
| OPA, LiteLLM, `verified-architecture` | **Cut** / refuse that name. Kernel name is `intent-kernel` for CAS+receipt only |
| cas-apply / Intent Kernel | **E-IK0** greenfield, deferred; D-00=B, D-01=b |

## 3. Cut list (no spec, no tickets, no “later in this epic”)

- Semantic + temporal indices; SPO claim graph; evidence planner
- Entire Intent Kernel write path (E-IK0 Implement; LiteLLM; OPA runtime)
- Large multi-tool MCP; MCP write (`replace_symbol_body` is Serena’s, not ours)
- Tags-as-product / Context Compiler without S2 ablation
- E-FACT0 warehouse — S1 is a **slice** (new predicates on the existing ledger)

## 4. Bloom (program)

| Level | Evidence |
| --- | --- |
| Remember | Serena tools `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `replace_symbol_body` `[Evidenced — oraios/serena tools.md @ 9cd33aa5]`; `metaResolutionEnabled() { none() }` `[Confirmed — Annotations.qll:112]` |
| Understand | ast-grep = source-text sensor; CodeQL pack = Spring-resolved facts when the DB is real; MCP here = read-only over Stage-0 artifacts |
| Apply | S0 = operator `uv` pin + MCP on the Java tree; S1 = extend `spring_signal_scan` / pack, not a new BC; S2 = invoke `doc-engine pipeline gates` + CodeQL + plant tests |
| Analyze | Adopt Serena; Embody pack + `dispatch_tool` root pin; Refuse index/SPO/kernel |
| Evaluate | False-green rows in each stage spec |
| Create | Tickets + Acceptance in S0–S2 |

DeepWiki Ask was **not** in this session’s MCP catalog. Cartography:
`https://deepwiki.com/oraios/serena` (indexed 2026-08-04). Primary docs used
instead of uncited summary.

## 5. Invariants (all stages)

`fail_under` **98.7** (cell 3.11 only) · complexipy ≤5 · LOC ≤225 · no `utils/` ·
descriptive CLI flags · OAS12: no MCP write in this repo · one Active tip.

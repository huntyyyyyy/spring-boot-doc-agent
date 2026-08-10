---
title: Finding — statement-split thrash → cascading CI red (2026-08-09)
status: closed — E-STK1 G1–G6 sensors Embodied (2026-08-09)
kind: process_incident
date: '2026-08-09'
tip_at_detection: 7fcb387
ci_run: 31334707945
related:
- docs/research/process/19-watch-stalker-agents-context-lean-2026.md
- docs/research/quality-backlog.md
- docs/design/concept-split-cohesion-design-2026-08-09.md
- src/doc_engine/ci/stalker_sensors/
backlog: P15.1 Done (E-STK1); P17.1 E-COH1 Active next
claim_tiers: Unknown
last_reviewed: '2026-08-10'
---

# Finding ledger: mechanical statement-split cascade

Structured stalker output (STK2). Not a chat dump. Sensors that would have
emitted these findings were Deferred with E-STK1 while Active tip was E-COH1.

## Sequence (commits / process)

| Step | Event | Failure |
| --- | --- | --- |
| 1 | `9353acf` E-STK0 Approve; E-STK1 Defer | Spec without sensors → no watch loop |
| 2 | `085fd72` E-COH0 Approve; Active E-COH1 | Cohesion bar; mechanical chops listed Never |
| 3 | `683656a` schema v6 HARD_STATEMENTS=20 | Policy moved; baselines not regenerated |
| 4 | Parallel Task agents (LOC/stmt) after pause | Multiple tip writers; gate-clearance goal-sub |
| 5 | `9775231` finish HARD_STATEMENTS≤20 | Prelude/core without return; Py3.10 f-strings; unbound `PY` |
| 6 | Reactive “ruff + ABI” fix request | Patch-only response |
| 7 | `7fcb387` ruff `--fix` + harness repair | Cleared F821/harness SyntaxError; F401 dropped façade `_` climb pokes; schema skew untouched |
| 8 | CI `31334707945` | quality 5≠6; size 2≠3; climb NameError/AttributeError; kitchen `PY` |

**Root:** Implement thrash without cohesion Spec discipline and without stalker
sensors that present gaps before another fix commit (STK5→STK2→STK6).

## Gap classes → E-STK1 sensors

| ID | Kind | Manifestation | Sensor (Embody when E-STK1 Active) |
| --- | --- | --- | --- |
| G1 | `ratchet_schema_skew` | code_quality 5≠6; size-ratchet 2≠3 | Compare code `SCHEMA_VERSION` vs committed JSON |
| G2 | `split_scope_break` | 14 climb prelude/core; earlier harness | AST: core loads Names assigned only in prelude, not passed |
| G3 | `facade_api_regress` | climb `facts._*`, `compliance._*`, etc. after F401 fix | AST: consumers load `module._attr`; façade must re-export or retarget |
| G4 | `collect_or_syntax` | kitchen `PY`; Py3.10 f-string unmatched `[` | `compileall` + `pytest --collect-only` on 3.10 and 3.12 for touched paths |
| G5 | `process_parallel_tip` | parallel split agents during COH0 pause | Backlog Active ID vs agent labels; refuse second tip writer |
| G6 | `policy_verify_incomplete` | statements ceiling bump alone | Schema-bump Verify pack: baseline `--update` + ABI domain smoke |

Refuse: LLM as fail_under; sensors rewriting oracle SoT (STK1).

## Disposition

- **Present:** this ledger + backlog P15 acceptance inputs for G1–G6.
- **Fixer (short-horizon, STK7):** restore façade aliases; repair prelude/core;
  import `PY`; regenerate baselines — after this ledger exists.
- **G6 partial (2026-08-09):** `check_code_quality` hard-fails statements ≤20 for
  `src/` + `tests/` only (aligns with size-ratchet package roots). Remaining
  `scripts/**` functions above 20 stay measured in the baseline as open debt —
  remediable under E-COH / a dedicated stream, not silent grandfather of product.
- **Post-merge (2026-08-09):** tip `#112` merged to `main` with remaining red.
  Local inventory still shows **4 G2 prelude/core leaks** + façade patch miss +
  CQ unit-test scope skew + collapsed soft band + obsolete metamorphic ratchet +
  docs path pin drift. **Research Spec DRAFT:** E-HOT0
  ([`process/21-…`](../process/21-post-merge-gate-repair-cohesion-2026.md),
  design [`post-merge-gate-repair-design-2026-08-09.md`](../../design/post-merge-gate-repair-design-2026-08-09.md);
  SoR bar raised to **≥10k★** for new external Adopt on this stream).
  **Stack rescope DRAFT:** E-STACK0
  ([`process/22-…`](../process/22-stack-rescope-10k-star-bar-2026.md)) —
  keep ≥10k pins; Confirmed exempt; Nx patterns for boundaries; no tool swap
  before E-HOT1 green.
  **No further product Implement until HOT1–HOT13 Approve** (STACK Approve is docs-parallel).
-   **E-HOT1 (2026-08-09):** Spike receipts
  [`2026-08-09-e-hot-r1-r4-spike-receipts.md`](2026-08-09-e-hot-r1-r4-spike-receipts.md);
  G2 return/pass + AST witness; CQ HOT5 slash-free scope; size soft-band test;
  cert patch-at-use; docs path pin. Metamorphic wrap ratchet **retained** (defect
  still moves set). **Verify:** `pre_pr --full` overall=pass. Disposition: **closed**.
  Next Active: **E-COH1** reshape.
- **Do not:** start full E-STK1 Implement in the same tip as deep E-COH1 without
  an explicit Active switch; more parallel statement/LOC agents; treat
  `ruff --fix` as Verify; push before local full-gate green.

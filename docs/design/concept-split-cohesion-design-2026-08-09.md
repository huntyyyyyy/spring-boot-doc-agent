---
category: Concept-split cohesion / tach-aligned modularity
status: DRAFT — SPEC GATE E-COH0 pending Approve of COH1–COH12
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/research/process/15-legacy-size-remediation-2026-frameworks.md
  - docs/research/modularity/12-pipeline-stage0-modularity-ports-2026.md
  - docs/research/modularity/16-scan1-astgrep-modularity-2026.md
  - docs/research/quality-backlog.md
  - tach.toml
do_not:
  - resume LOC/statement thrash as Active tip until this Spec is Approved
  - treat façade re-export of private `_` helpers as a finished interface
  - name modules residual bins (basic, misc, part2, helpers, inventory_drift grab-bags)
  - dual-wire import-linter + tach without LEG-S1
  - raise LOC/statement/complexipy ceilings to clear debt
spec_gate: DRAFT E-COH0 (2026-08-09) — COH1–COH12 pending Approve
---

# Design memo: cohesion-first concept splits (post-MOD-S1 tip audit)

> **DRAFT — SPEC GATE E-COH0**
>
> Tip audit of recent ≤225 / ≤20 splits found **concept-named seams with residual
> mechanical smells** (private re-export façades, mixed helper bins). User direction:
> **another design pass** before more size thrash. Do not Approve-by-silence —
> stamp Approve of **COH1–COH12** to unlock E-COH1 remediation under E-TACH0 order.

**Spec record**

| Field | Value |
| --- | --- |
| Research SoT | [`modularity/20-tach-dependency-blueprint-2026.md`](../research/modularity/20-tach-dependency-blueprint-2026.md) (Jun–Aug 2026) |
| Prior Spec | E-LEG0 / E-MOD* / E-SCAN1 / E-TACH0 (draft) |
| Branch / PR | `cursor/e-doc1-research-taxonomy-61f3` / [#112](https://github.com/huntyyyyyy/spring-boot-doc-agent/pull/112) |
| Backlog | P17 below |

**Claim tiers:** `[Evidenced]` primary docs/tools · `[Confirmed]` this tip · `[Unknown]` needs measure.

---

## 1. Problem

Size gates (LOC≤225, statements≤20, complexipy≤5) are **necessary but not sufficient**.
A tip that only optimizes those numbers can still ship:

| Smell (tip audit) | Example `[Confirmed]` | Why it fails modularity |
| --- | --- | --- |
| Façade = private re-export warehouse | `registry.py` / `support.py` re-export many `_` helpers | Callers still couple to internals; tach `[[interfaces]]` would fail |
| Residual helper bin | `inventory_drift.py` mixes `py_mod` + inventory + drift | Three concepts, one file — LOC-shaped bag |
| “Other” hook bucket | `registry_hooks_basic` = non-absence/recall rates | Name encodes leftover, not domain |
| Split-before-edge map | BC cycles `pipeline`↔`scanning` still present | Depends_on map cannot land (E-TACH0 TACH4) |

**Root cause:** MOD-S1 was executed as **gate clearance** under Active size pressure, not as **dependency-blueprint design** (user: dependencies as primary structure; research 20).

---

## 2. One-page verdict

| Question | Answer |
| --- | --- |
| Keep chopping until offender maps are empty? | **No — pause thrash.** Finish **E-COH0 design Approve**, then remediate under cohesion bar + E-TACH0 order. |
| Were tip splits worthless? | **No.** Concept names / vertical slices are a better starting point than `part2`; treat as **provisional debt** to reshape, not delete. |
| Primary SoR for structure? | **Declared dependencies + public interfaces** (tach), not LOC alone. `[Evidenced]` research 20 |
| Mechanical cut-and-paste? | **Refuse** as Accept criteria — even if LOC passes. |

---

## 3. Design principles (locked by Approve)

1. **One concept per module** — name must state the concept; refuse `basic` / `misc` / `helpers` / multi-concern leftovers.
2. **Façade = public surface only** — `__all__` / tach `expose` lists the contract; private helpers stay unexported.
3. **Split along dependency edges**, not line counts — target future BC layers (`scanning`, `pipeline`, `query`, `ci`, `tools`, `core`, …).
4. **Size gates verify; they do not design** — ≤225 / ≤20 / ≤5 are Accept checks after a seam map, not the seam map.
5. **Provisional tip modules** may remain until E-COH1; new splits must meet this bar immediately.
6. **Tests:** prefer separate methods for distinct contracts (E-LEG intentionality); mega-test statement chops without renaming contracts are Defer.

---

## 4. Spec decisions (COH1–COH12) — pending Approve

| ID | Decision |
| --- | --- |
| **COH1** | Further size remediation is **blocked** as Active tip work until E-COH0 Approve (except hotfix for broken imports/CI) |
| **COH2** | Accept a split iff: (a) concept-named, (b) single responsibility, (c) façade exports only public API, (d) LOC/stmts/complexipy pass |
| **COH3** | Refuse residual bins; rename/split `inventory_drift`-class modules on touch |
| **COH4** | Refuse façades whose primary job is re-exporting private `_` callables to preserve deep imports — migrate callers to the concept module or a true port |
| **COH5** | Seam map for each BC wave written **before** file moves (table: module → responsibility → allowed deps) |
| **COH6** | E-COH1 Implement order follows E-TACH0: cycle-break → layers → depends_on + interfaces (do not invert) |
| **COH7** | `tach sync` proposes; seam map + Spec Approve; never sync-as-architecture |
| **COH8** | Statement≤20 / LOC≤225 / complexipy≤5 remain hard; **no grandfather** of new offenders |
| **COH9** | Existing tip concept modules are **provisional** — tracked as COH debt, not “Done modularity” |
| **COH10** | Test ≤20 work uses intentional method splits / support concept modules — not assert-packing |
| **COH11** | Dual import-linter stays Deferred (LEG-S1); tach is sole fitness tool |
| **COH12** | CONTRIBUTING size remediation cites this memo + research 20 as the cohesion bar |

---

## 5. Epic sketch

### E-COH0 — Spec gate (this memo)
- **Exit:** `status: APPROVED E-COH0` + COH1–COH12 stamped; backlog P17.0 Approved.

### E-COH1 — Reshape provisional tip modules
| ID | Title | Acceptance |
| --- | --- | --- |
| COH1-1 | Inventory provisional façades/bins on tip | markdown table in research or this memo appendix |
| COH1-2 | Split/rename residual bins (`inventory_drift`, `registry_hooks_basic`, …) | COH2–COH4 green on touch |
| COH1-3 | Narrow façades to public `__all__`; migrate deep `_` imports | no private re-export warehouse |
| COH1-4 | BC cycle-break prep (ports) | one-way edges ready for E-TACH1 |

### E-COH2 — Align with E-TACH1/2
After E-TACH0 Approve: layers then depends_on+interfaces using COH seam maps.

**Invariants:** constitution gates; one tip writer; no utils/.

---

## 6. Adversarial checklist

- [ ] Does Approve re-open LOC thrash without seam maps? — **Forbidden (COH1, COH5).**
- [ ] Can a module pass LOC with three concepts? — **No (COH2–COH3).**
- [ ] Is “stable import path” an excuse for exporting privates? — **No (COH4).**
- [ ] Does this weaken ≤20/≤225? — **No (COH8).**
- [ ] Parallel tip with E-CQL1/E-STK1? — **No;** one Active stream.

---

## 7. Exit

Human **Approve COH1–COH12** (or explicit subset). Until then: **Active tip = design/Spec only** for modularity; size offender paydown waits on E-COH1 under this bar.

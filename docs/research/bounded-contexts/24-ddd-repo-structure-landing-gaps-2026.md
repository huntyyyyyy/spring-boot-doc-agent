---
title: E-REPO0 gap analysis — what will not land at Implement/Test
status: DRAFT amend — honest landing risks for packet 21+22+23
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
parent:
  - docs/research/bounded-contexts/21-ddd-repository-structure-options-2026.md
  - docs/research/bounded-contexts/22-ddd-repo-structure-quality-deepdive-2026.md
  - docs/research/bounded-contexts/23-ddd-repo-structure-capability-backcast-2026.md
related:
  - docs/design/concept-split-cohesion-design-2026-08-09.md
  - docs/research/bounded-contexts/20-tach-dependency-blueprint-2026.md
  - tach.toml
do_not:
  - treat DOMAIN_MAP.md alone as “structure done”
  - claim tach interfaces landed while pipeline↔scanning cycles remain
  - use map-only tickets as cover for skipping façade poke / import inventory
spec_gate: DRAFT E-REPO0 gap amend (2026-08-10)
---

# Implementation / test landing gaps (E-REPO0)

**User concern (valid):** the research packet describes destinations; it under-specifies
what **actually has to pass** in Implement → Verify, and several recommended moves
**cannot land** on today’s graph without prior work that the packet treated as
“later.”

This amend is the adversarial landing list. Claim tiers as usual.

**Wave 0.5 (2026-08-10):** research domain renamed `modularity/` → `bounded-contexts/`;
`DOMAIN_MAP` §4 lists nest/collapse candidates (tools→BC, dual skills). Physical
`src/` dissolve still blocked by cycles below.

---

## 0. One-page verdict

| Concern | Answer |
| --- | --- |
| Will “Wave 1 deep BC + tach” land if ordered tomorrow? | **No.** `pipeline`↔`scanning` mutual imports and `tools`→{pipeline,query,scanning} fan-in still exist. `[Confirmed]` tip AST inventory; E-COH0 / TACH4 already say depends_on cannot land first. |
| Will Wave 0 (DOMAIN_MAP) look green but not prove structure? | **Mitigated 2026-08-10:** inventory + `behavior:tools_bc_inventory_covers_modules` + CONSTRAINTS verify. Map still ≠ physical restructure Done. |
| Biggest silent fail mode? | Move files, keep barrel re-exports, tests still import deep paths → **façade cosplay**; size/cov pass; modularity does not. |
| What *can* land soon with real tests? | Cycle-break ports (E-COH1/E-TACH prep), façade poke expansion, tools→BC **inventory JSON** with claims, domain markers (already E-TEST) — not root renames. |

---

## 1. Confirmed blockers on tip (not theoretical)

| Gap ID | Fact | Why Implement stalls |
| --- | --- | --- |
| **G-CYCLE** | Cross-package edges include `pipeline↔scanning` and `tools→pipeline,query,scanning` | tach `depends_on` / layers (**Possibility 2/F**) fail or require ignore debt; E-TACH0 TACH4 / E-COH0 already flagged |
| **G-TEST-COUPLE** | **118** test files mention `doc_engine.tools` or `tools/` | Dissolving `tools/` is a **test rewrite epic**, not a `git mv`; monkeypatches and `-m doc_engine.tools.*` break |
| **G-INVOKE** | Public invoke SoT is `python -m doc_engine.tools.<mod>` + skills/CI | Renaming packages without **stable façade modules** (re-export or CLI alias) breaks operator pilot + Action |
| **G-ACTIVE** | Active tip is **E-COH1**, E-REPO0 still DRAFT | Ordering E-REPO1 Implement without Approve = process refuse + parallel tip risk |
| **G-COH** | Tip modules are **provisional**; façade≠warehouse is the bar | Structure moves that only relocate LOC offenders fail COH Accept even if folders look right |

`tach check` is green **today** because only coarse modules `doc_engine`/`stf` + cycle forbid at that grain — **not** because BC edges are clean. Finer map is exactly what cannot land yet. `[Confirmed]`

---

## 2. Spec underspecification (will fake-green)

| Gap ID | What memos say | What’s missing for Verify |
| --- | --- | --- |
| **G-MAP** | “Publish DOMAIN_MAP.md” | No schema; no claims `contains:`; no test that every `tools/*.py` row appears; no CODEOWNERS generator |
| **G-TRUTH** | Label SoR/derived/sensor | No machine-checkable path allowlist; climb could still write `coverage.xml` until existing 16-A tests catch it — labels add **zero** new bite |
| **G-PSMELL** | REPO-S3 PairSmell inventory | No committed script, window (90d?), co-change data source (`git log`?), threshold, or fixture; “inventory” can be a vibes table |
| **G-STAGE** | Dissolve via stage dialect | No mapping table tools→stage with owners; no rule for files that are both gate + scan helper |
| **G-BASE** | Multi-base Polylith pattern | No pyproject/extras sketch; no test that Action/plugin import only façades |
| **G-PACK** | Agent packs | No equality strategy vs `adapters/claude/skills` ↔ root `skills/` mirror CI |
| **G-ACCEPT** | Epic tickets list Acceptance one-liners | No pytest node ids, no `pre_pr` recipe, no rollback criterion |

**Pattern:** research optimized **ranking**; it deferred **executable Accept**. That is the implementation gap you are smelling.

---

## 3. What “testing” cannot prove (even after moves)

| Claim we might want | Reality |
| --- | --- |
| “Structure screams Spring-doc” | No automated scream test; only human `ls` review |
| “InCol fixed” | Without co-change + import metrics job, fixed is narrative |
| “Agents load less context” | No context-token benchmark in CI; E-STK not implemented |
| “Ready for HttpLLM / multi-repo” | H3 capabilities have no product Spec; structure prep is speculative |
| “Deep modules” | tach interfaces can enforce import paths; **cannot** enforce conceptual depth (Ousterhout) |

So even a green PR can fail the *intent* of memos 22–23 unless Accept is narrowed to **enforceable** predicates (tach, poke, claims, invoke smoke).

---

## 4. Landing sequence that can actually pass gates

Ordered so each step has a **boolean Verify** before the next:

| Step | Work | Verify (must exist or be written in same tip) | Lands without… |
| --- | --- | --- | --- |
| **L0** | Approve E-REPO0 packet **including this gap amend** | Spec status flip | — |
| **L1** | Tools→BC/stage **inventory artifact** (JSON/CSV in docs or scripts) + claims path | `check_repo_claims` row count = tools py count | Any `git mv` |
| **L2** | Break `pipeline`↔`scanning` via ports/façades (E-COH1 / TACH prep) | Import inventory one-way; façade poke | Full tools dissolve |
| **L3** | tach **layers** only (not full depends_on matrix) | `tach check` green | Deep BC renames |
| **L4** | One tools cluster → BC **with stable `-m` shim** | `python -m doc_engine.tools.<old>` still works; targeted pytest | Big-bang tools/ |
| **L5** | tach `[[interfaces]]` on that BC | Deep import fails in CI | Repo-wide interfaces |
| **L6** | Expand; only then consider physical truth zones / bases | Prior steps green on main | Parallel root rename |

Anything that jumps to L6 from L0 is what “will not land.”

---

## 5. Concrete missing deliverables to add before Implement

Treat as **Spec debt** (tickets), not prose:

1. **`tools_bc_inventory` schema** + generator script + claims.  
2. **Stable invoke policy:** shims required N releases / forever for `doc_engine.tools.*`.  
3. **Cycle-break ticket** explicitly prerequisite of E-REPO1 Wave 1 (link E-COH1).  
4. **Accept template** per move: `ruff` + size + complexipy + façade poke + `tach check` + listed pytest paths + one `doc-engine pipeline` smoke.  
5. **REPO-S3 method:** ast import graph + optional `git log --follow` co-change; time-box; output format.  
6. **Non-goals test:** ban PR description “reorganized folders” without L1–L5 evidence.

---

## 6. Risk if told “implement the research now”

| If you mean… | Likely outcome |
| --- | --- |
| Wave 0 map only, no claims bite | Lands as docs; **false sense of Done** |
| Wave 0 map + inventory + claims | Lands; real but small |
| Wave 1 dissolve `tools/` + tach interfaces | **Stalls** on G-CYCLE / G-TEST-COUPLE or ships shims+debt |
| Root scream / physical truth / polylith folders | **Long red tip**; H1 calibration blocked; high revert pressure |
| “Just move tests under BC dirs” | 118+ files + markers churn; E-TEST said markers first for this reason |

---

## 7. Spec deltas

| ID | Decision | Stance |
| --- | --- | --- |
| **REPO21** | E-REPO1 Wave 1 **blocked on** documented one-way `pipeline`/`scanning` edge (or explicit Spike waiver) | **Embody** |
| **REPO22** | DOMAIN_MAP without inventory+claims predicate = **not** Accept for structure epic | **Adopt** |
| **REPO23** | Every package move keeps `doc_engine.tools.<mod>` invoke green unless deprecation Spec | **Adopt** |
| **REPO24** | Research rankings are not Implement tickets until §5 deliverables exist | **Embody** |

---

## 8. Bottom line

Your instinct is right: **21–23 over-specify destinations and under-specify landing gear.**  
The honest path is not “more folder options” — it is **L1–L5 above**, mostly overlapping E-COH1/E-TACH0, with structure research demoted to a **routing map** until cycles, shims, and inventory are real.

Approve E-REPO0 only with eyes open: the valuable near-term Implement is **cohesion + cycle-break + inventory**, not Possibility 2 as a big-bang.

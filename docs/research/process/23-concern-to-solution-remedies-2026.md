---
title: E-SOL0 — Concern→solution map (DDIA labels → 2026 effective remedies)
status: DRAFT Spec — pending Approve of SOL1–SOL10
research date: 2026-08-09
research_window: 2026-06-01 → 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`)
related:
  - docs/design/ddia-north-star/INDEX.md
  - docs/research/process/21-post-merge-gate-repair-cohesion-2026.md
  - docs/research/process/22-stack-rescope-10k-star-bar-2026.md
  - docs/research/process/19-watch-stalker-agents-context-lean-2026.md
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md
  - docs/research/quality-backlog.md
do_not:
  - treat DDIA page ids as Accept criteria without a named remedy mechanism
  - invent new SoT floors from LLM-judge or scoped Cover%
  - dual-wire Sonar/Spec Kit/Nx as runtime SoT
  - raise constitution ceilings to “make room”
spec_gate: DRAFT E-SOL0 (2026-08-09) — SOL1–SOL10 pending Approve
gh_sor_bar: "≥10000★ for new external SoR; Confirmed pins Embody-continue (HOT13/STACK)"
critique: "Human 2026-08-09: north-star tables described problems without solution mechanisms research shows effective"
---

# Principal memo: from DDIA *concern labels* to *effective remedies*

**Question.** When we map work to DDIA north-star pages (`sor-vs-derived`,
`rel-gate-needs-witness`, …), how do we stop at diagnosis and instead **Adopt
mechanisms that 2025–2026 research and high-adoption practice show work** for
those concerns in *this* product?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Was the critique fair? | **Yes.** E-HOT1’s DDIA table named failure *classes* but Accept criteria stayed “fix the instance.” Diagnosis ≠ remedy. `[Confirmed]` |
| What research says works for architectural drift? | **Architecture fitness functions** — automated, continuous, objective checks of *invariants* (not drawings). Ford evolutionary architecture lineage + 2026 fitness-function practice. `[Evidenced]` |
| What works for dual-write / two SoRs? | **Single atomic write + derive the rest** (outbox/CDC pattern transferred to *artifacts/APIs*): one SoR, derived views recomputed; refuse parallel authoritative APIs. `[Evidenced]` arXiv [2608.00501](https://arxiv.org/abs/2608.00501) + industry outbox doctrine |
| What works for “gate not vacuous”? | **Witness + mutation/metamorphic adequacy**, not Cover% alone. Repo already Embody mutmut advisory + metamorphic; E-QA SMS/MC are sensors. `[Evidenced]` + `[Confirmed]` |
| What works for safe reshape under agents? | **Characterization net first → one seam → structural verify** (Feathers + 2026 agent-refactor practice). `[Evidenced]` |
| What works for recurring G2-class gaps? | **Standing fitness function** (AST leak check in CI) + stalker ledger → Spec — not one-off patches. E-HOT shipped witness test; E-STK1 sensors are the generalizer. `[Confirmed]` + `[Evidenced]` E-STK0 |

---

## 1. The anti-pattern we fell into

```text
Concern (real) → DDIA page id → "Application: don't dual-write"
                              → Implement: patch the one failing test
```

That path **describes** and **locally clears** but does not **install the remedy
class** research recommends (fitness function / single-write / characterization
net / adequacy witness).

**Required shape going forward**

```text
Concern → DDIA lens (optional vocabulary)
       → Named remedy mechanism (paper/tool/pattern + ★/Confirmed)
       → Accept = mechanism installed or Explicit Defer with exit criterion
```

---

## 2. Concern → remedy matrix (this product)

| Concern (DDIA id) | Effective remedy (research / practice) | Already in repo? | Next Adopt |
| --- | --- | --- | --- |
| **SoR vs derived** (`sor-vs-derived`) | One authoritative artifact/API; views recompute; never LWW two writers | Oracle `coverage.xml` vs climb XML **16-A**; cert report derived | Document every new gate as SoR\|derived in Spec; refuse second enum/string API (E-HOT cert) |
| **Dual-write** (`replication-lag-and-lww`) | Eliminate dual write: single commit + derived projection (outbox *pattern*) | PathCohesion single-writer; tip one writer | Apply to façades: **one binding site** for doubles (patch-at-use); façade re-export ≠ second SoR |
| **Gate needs witness** (`rel-gate-needs-witness`) | Fitness function + mutant/metamorphic kill evidence | `pre_pr`, mutmut advisory, metamorphic suite, G2 AST witness | Promote G1–G6 to E-STK1 **sensors** (not chat); adequacy Q2 witness checklist on climb |
| **Vacuous Cover%** (`coverage-gates`) | Adequacy sensors ≠ floor; mutation/metamorphic | E-QA0–2 Done | Keep Cover% necessary-not-sufficient; optional MC/SMS as **advisory** only |
| **Claims drift** (`claims-and-status-drift`) | Executable predicates on claims (`verify:`) | `check_repo_claims.py` | Keep; path pins follow migrate (HOT8) |
| **Maintainability / chops** (`maintainability-…`) | Fitness on **structure** (cycles, public surface, stmt leaks) + characterization before reshape | tach cycles; size/complexipy; E-COH bar; G2 witness | E-COH1: seam map **before** moves; E-TACH0: Nx-pattern interfaces via Confirmed tach vehicle |
| **Process / tip thrash** | Spec→Impl→Verify; watch≠fixer; rotate focus | E-STK0 Approved; one tip writer | E-STK1 when Active — sensors present gaps *before* another fix commit |

### 2.1 Remedy mechanisms (what “effective” means here)

| Mechanism | What it does | Evidence | Product stance |
| --- | --- | --- | --- |
| **Architecture fitness function** | Encodes invariant (“no prelude leak”, “no cycle”, “public surface only”) as CI-hard check | Ford evolutionary architecture; 2026 fitness-function practice; HICSS 2026 research-software fitness | **Embody** tach cycles + G2 witness; **Adopt** more structural fitness for G1/G3/G6 under E-STK1 |
| **Single-write / derive** | One SoR mutation; everything else projection | Outbox/CDC doctrine; arXiv 2608.00501 (recovery bounds) | **Embody** for coverage/cert/policy; map “outbox” → “write oracle once; climb/summary derive” |
| **Characterization net** | Lock current behavior *before* reshape; never “fix while extracting” | Feathers; 2026 agent-refactor writeups | **Embody** for E-COH1; façade poke (E-FAC0) |
| **Mutation / metamorphic adequacy** | Prove gates kill defects, not just lines | Mutmut; metamorphic coverage (2025); SMS (2026) exploratory | **Embody** advisory mutmut + metamorphic; **Refuse** as fail_under substitute |
| **Sensor → ledger → Spec** | Watch presents gaps; humans Spec; fixer separate tip | E-STK0 / react-doctor pattern | **Adopt** E-STK1 when Active |

---

## 3. Re-score of E-HOT1 remedies (honesty)

| HOT fix | Was it a *mechanism* or an *instance patch*? | Upgrade |
| --- | --- | --- |
| G2 return/pass | Instance repair | **Mechanism installed:** `test_g2_prelude_core_scope` fitness function — keep in CI forever |
| CQ HOT5 | Predicate SoR clarified | Add **characterization matrix test** (done) — treat matrix as SoR doc |
| Cert patch-at-use | Instance of single-binding | Document as **façade poke rule**: doubles bind where name is used (pytest ≥10k★) |
| Wrap ratchet | Correct *instance* keep | Mechanism still missing: **fix first-line match** or accept permanent metamorphic exception with CONSTRAINTS Archive — Defer product fix |
| Docs path | Claims drift instance | Mechanism already `check_repo_claims` — path pins are characterization |

**Lesson:** every epic Accept row must name the **mechanism** column, not only the file touch.

---

## 4. Spec decisions (SOL1–SOL10) — pending Approve

| ID | Decision |
| --- | --- |
| **SOL1** | DDIA page ids are **vocabulary only**; Spec Accept requires a named remedy mechanism from §2.1 or Explicit Defer |
| **SOL2** | Architecture fitness functions are the default remedy for structural concerns (G1–G3, cycles, public surface) |
| **SOL3** | Dual-write concerns Adopt **single-write + derive**; refuse parallel authoritative APIs (str+enum, climb+oracle same path) |
| **SOL4** | Gate concerns Adopt **witness fitness + mutation/metamorphic adequacy**; Cover% remains necessary floor only |
| **SOL5** | Reshape concerns Adopt **characterization net → one seam → structural verify** (E-COH1 bar) |
| **SOL6** | Recurring incident classes Adopt **sensor → ledger → Spec** (E-STK1) rather than reactive tip thrash |
| **SOL7** | Research memos must include a **Concern→Remedy→Accept** table; diagnosis-only tables are incomplete |
| **SOL8** | ≥10k★ bar still binds *new* tool Adopts; Confirmed pins may host fitness functions (tach, pytest, ast-grep) |
| **SOL9** | E-COH1 / E-STK1 / E-TACH0 Specs must cite SOL remedy ids, not only DDIA page ids |
| **SOL10** | Wrap-annotation first-line defect: Defer product fix; keep ratchet; do not pretend HOT7 “fixed” it |

---

## 5. Epic sketch

### E-SOL0 — Spec gate (this memo)

Exit: Approve SOL1–SOL10; backlog P20.0.

### Follow-ons (ordered, one Active)

| Epic | Uses remedies | Notes |
| --- | --- | --- |
| **E-STK1** | SOL2, SOL4, SOL6 | G1–G6 as fitness sensors |
| **E-COH1** | SOL5, SOL2 | Characterization + seam map before moves |
| **E-TACH0 Amend** | SOL2, SOL8 | Nx-pattern SoR; tach Confirmed vehicle |

---

## 6. Adversarial checklist

- [ ] Does a Spec row only cite a DDIA id? — **Fail SOL1.**
- [ ] Is Cover% used as proof a structural gate works? — **Fail SOL4.**
- [ ] Are we adding a second authoritative API to “make tests green”? — **Fail SOL3.**
- [ ] Is reshape starting without a characterization net? — **Fail SOL5.**
- [ ] Is the “solution” another one-off patch for a class G2 already witnessed? — **Fail SOL6** unless expanding the fitness function.

---

## 7. Exit

**E-SOL0 DRAFT** until human Approve of SOL1–SOL10.
This memo answers the critique: north-star pages stay useful as *lenses*;
**research-backed remedies** (fitness functions, single-write/derive, characterization,
mutation/metamorphic witnesses, sensor→Spec) become the load-bearing Accept path.

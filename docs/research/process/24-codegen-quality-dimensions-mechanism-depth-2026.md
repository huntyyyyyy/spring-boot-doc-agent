---
title: E-CGQ0 — Codegen-quality dimensions + remedy-mechanism depth
status: APPROVED E-CGQ0 (2026-08-09) — CGQ1–CGQ10; tip-grounding MCP vehicle Explicit
  Defer (E-GND)
date: '2026-08-09'
research_window: 2026-06-01 → 2026-08-09
claim_tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`)
related:
- docs/research/process/23-concern-to-solution-remedies-2026.md
- docs/design/ddia-north-star/meta/effective-remedies.md
- docs/research/process/25-tip-grounding-mcp-2026.md
- docs/research/coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md
- docs/research/process/14-facade-poke-research-hooks-2026.md
- docs/research/process/19-watch-stalker-agents-context-lean-2026.md
- docs/research/se-quality-synthesis-2026-08-08.md
- docs/research/quality-backlog.md
do_not:
- Embody new fitness / ETL / characterization nets from remedy *labels* alone
- treat Cover% or LLM-as-judge as generation or structural proof
- adopt Spec Kit WorkflowEngine / Sonar / dual arch linters as SoT
- raise fail_under / LOC / complexipy ceilings
- implement E-GND1 before E-STK1 green cycle
spec_gate: APPROVED E-CGQ0 (2026-08-09) — CGQ1–CGQ10
gh_sor_bar: ≥10000★ for new external SoR; Confirmed pins Embody-continue
critique: 'Human 2026-08-09: (1) remedy labels without theory/math/algo/DS/ETL → vague
  codegen start; (2) post-hoc CI misses pre-generation dimensions that raise agent
  code quality.'
last_reviewed: '2026-08-10'
---

# Principal memo: codegen quality controls + mechanism depth

**Question.** What must an agent *know and probe* before generating code in this
repo so Accept criteria are not vague labels — and which missing dimensions,
beyond existing CI floors, research shows improve generated-code quality?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Was installing remedy *ids* into north-star enough? | **No.** Ids are vocabulary. Codegen from labels without depth rows recreates the DDIA diagnosis problem. `[Confirmed]` |
| Are post-hoc gates (Cover%, size, complexipy, claims) sufficient for agent quality? | **Necessary, not sufficient.** They catch after generation; they do not force grounding / Spec completeness / independent Verify. `[Evidenced]` + `[Confirmed]` |
| What research says reduces context blindness? | Phase-scoped **read-only repository probing** + validation hooks on Spec/Plan/Tasks (arXiv [2604.05278](https://arxiv.org/abs/2604.05278)). `[Evidenced]` — Adopt *recipe*; Refuse Spec Kit WorkflowEngine runtime (STACK/synthesis). |
| What research says correctness benchmarks miss? | Production-readiness / maintainability / reviewability dims need human or structured review beyond unit pass (arXiv [2605.09059](https://arxiv.org/abs/2605.09059)). `[Evidenced]` — Adopt selective sensors; advisory for colleague-accept; refuse as fail_under. |
| When may new fitness/ETL land? | Only after **mechanism depth rows** (§2) + **CGQ3 Accept** (Concern → Remedy → Depth cite → Witness). |

```text
PRE-GENERATION              DURING                    POST
─────────────────           ──────                    ────
Structural grounding   →    Contract fidelity    →    Independent Verify
Mechanism depth        →    Effect / blast map   →    Spec↔witness trace
Spec completeness      →                              Existing CI gates
Context bundle
```

---

## 1. Source verification (hype filter)

| Claimed source | Result | Tier |
| --- | --- | --- |
| Ford / Parsons / Kua — architectural fitness function | Primary book definition: objective integrity assessment of architectural characteristic(s); triggered vs continual | `[Evidenced]` |
| ArchUnit layeredArchitecture / dep graph | Bytecode→structure; whitelist layer rules; cycle/slice checks | `[Evidenced]` |
| arXiv [2608.00501](https://arxiv.org/abs/2608.00501) dual-write recovery | Isabelle/HOL; information bound: crash-side state cannot decide sink acceptance; outbox/CDC moves dual-write to relay | `[Evidenced]` |
| Kleppmann dual-write / derived data | SoR + derive views; refuse LWW as integrity merge | `[Evidenced]` (book) + `[Confirmed]` 16-A |
| Mutation theory (DeMillo CPH + coupling; MS / MSI) | MS = killed / (total − equivalent); equivalence undecidable; MSI = killed/total lower bound | `[Evidenced]` |
| Metamorphic testing (Chen; Segura survey) | MR over multiple executions; alleviates oracle problem | `[Evidenced]` |
| Feathers WEWLC — seams, characterization, effect analysis | Pin actual behavior; seam + enabling point; effect sketch before change | `[Evidenced]` |
| arXiv [2604.05278](https://arxiv.org/abs/2604.05278) Spec Kit Agents | Context-grounding discovery + validation hooks; +0.15 judged quality; 99.7–100% test compat | `[Evidenced]` |
| arXiv [2605.09059](https://arxiv.org/abs/2605.09059) LLM code quality eval | Correctness ≠ production-ready; structured human review dims | `[Evidenced]` |
| E-STK0 / react-doctor pattern | Sensor → ledger → Spec; watch≠fixer | `[Confirmed]` + pattern `[Evidenced]` |
| HICSS 2026 research-software fitness | Cited in SOL; full paper ID not re-fetched this pass | `[Unknown]` as standalone ID — Ford lineage sufficient for product stance |
| DeepWiki as architecture SoT | Cartography only | Not SoR |

---

## 2. Remedy-mechanism depth (traversal-ready)

Each subsection is the **depth row** CGQ2 requires before Embody of *new* instances.
Existing Embodied gates (tach cycles, G2 witness, 16-A, metamorphic, claims) stay;
new ones need these rows cited in Accept.

### 2.1 `fitness-function`

| Lens | Content |
| --- | --- |
| **Theory** | Evolutionary architecture: guided incremental change protected by objective assessments of named dimensions (Ford et al.). Categories: triggered vs continual; atomic vs holistic. |
| **Mathematics** | Prefer **boolean predicates** \(P: Artifact \rightarrow \{0,1\}\) for merge SoT. Scalar scores \(s \in [0,1]\) are sensors only unless Spec locks a threshold *and* fail direction. Composition: conjunction of hard predicates (CI AND), not weighted averages as floors. |
| **Algorithms / DS** | Build a **dependency graph** \(G=(V,E)\) (modules/packages as nodes; imports/calls as edges). Rules = forbidden subgraphs / layer whitelist paths (ArchUnit pattern). AST walk for name-leak (G2): parse prelude+core → free names vs passed params. |
| **ETL** | Fitness reads **committed tree + artifacts**, not chat. Report is derived; pass/fail is SoR for the gate. |
| **Impl (this CLI)** | Vehicles: pytest, tach (cycles Embodied), `ast`/`ast-grep`, `check_repo_claims`. ≥10k★ bar; Confirmed tach/complexipy exempt per STACK. |
| **Traversal checklist** | (1) Which architectural dimension? (2) Predicate or score? (3) Witness that fails closed? (4) Graph or AST SoR path? (5) Triggered (CI) or continual? |
| **Stance** | **Embody** existing; **Adopt** new only with depth cite + witness; **Refuse** drawings/README-only; **Refuse** dual arch linters. |

### 2.2 `single-write-derive`

| Lens | Content |
| --- | --- |
| **Theory** | Dual-write = two authorities without one commit. Remedy: one durable SoR write; derived images from committed history (outbox/CDC *pattern*). [2608.00501] proves recovery still faces sink-acceptance information bound at the relay — derivation does not dissolve exactly-once; it relocates it. |
| **Mathematics** | History \(H\), frontier \(f\), materialization \(\mathsf{Src}(b,H,f)\). Downstream clean iff \(\mathsf{Src}(b,D,f)=\mathsf{Src}(b,H,f)\) on scoped keys. Crash-side state alone cannot decide sink acceptance (information bound). |
| **Algorithms / DS** | SoR append/write API; derived **fold** function \(v = F(SoR)\); no second writer of the same key. Relay cursor / generation if async (usually N/A for batch cert/coverage). |
| **ETL** | Oracle `coverage.xml` write once; climb XML distinct path (**16-A**). Certification = derived fold over stage/gate facts — not LWW merge. Claims `derived:` blocks recompute counts. |
| **Impl** | PathCohesionGuard; `certification_finish`; refuse parallel str+enum authoritative APIs. |
| **Traversal checklist** | (1) Single writer of the fact? (2) Rebuild command for view? (3) On disagreement, who wins? (4) Are we inventing a second SoR to make tests green? (5) If relay exists, what is sink acceptance evidence? |
| **Stance** | **Embody** 16-A + cert fold; **Adopt** patch-at-use as binding discipline; **Refuse** silent LWW; Kafka/Debezium runtime **Refuse** (pattern transfer only). |

### 2.3 `characterization-net`

| Lens | Content |
| --- | --- |
| **Theory** | Feathers: characterization pins *actual* behavior before change; seam = place to alter behavior without editing that place; enabling point chooses behavior; effect analysis lists observable effects. |
| **Mathematics** | Pin set \(C = \{(x_i, y_i)\}\) observed under harness. Refactor \(T\) is characterization-safe if \(T(x_i)=y_i\) for all pins (behavioral equivalence on \(C\), not full semantic equivalence). |
| **Algorithms / DS** | Inventory seams (object/link/preprocess; prefer object/DI/params). Effect sketch: returns, param mutation, globals, filesystem, subprocess. Poke-surface set of patched attrs (E-FAC0). |
| **ETL** | Golden / snapshot artifacts are **derived pins**, not SoR of intent. Spec intent may later diverge deliberately with Explicit Defer. |
| **Impl** | pytest characterization; façade poke gate; E-COH bar before reshape. |
| **Traversal checklist** | (1) What behavior is pinned? (2) Where is the seam/enabling point? (3) Effect list for the change locus? (4) One seam per PR theme? (5) Are we “fixing while extracting”? |
| **Stance** | **Embody** for E-COH1; **Refuse** reshape without net; ApprovalTests zoo **Defer**. |

### 2.4 `adequacy-witness`

| Lens | Content |
| --- | --- |
| **Theory** | Cover% = execution footprint (necessary). Mutation: CPH + coupling → simple mutants; MS adequacy. Metamorphic: MR \(R(I,I',O,O')\) without concrete oracle. See also [`coverage-quality/09`](../coverage-quality/09-test-adequacy-vs-coverage-inflation-2026.md). |
| **Mathematics** | \(\mathrm{MS} = K / (T - E)\); \(\mathrm{MSI} = K/T\) (lower bound). Cover% monotone set function ≠ submodular mutant utility. MR violation ⇒ fault; satisfaction ⇏ full correctness. |
| **Algorithms / DS** | Mutant operator set; kill matrix test×mutant; MR transformer + relation checker; planted counterexample fixtures (positive/negative polarity). |
| **ETL** | Mutmut/metamorphic reports = **sensors**; oracle Cover% remains boolean floor. Never promote MSI to fail_under without Spec. |
| **Impl** | Metamorphic suite Embodied; mutmut advisory; E-QA SMS/MC sensors; gate mutators. |
| **Traversal checklist** | (1) What property must fail closed? (2) Witness path + polarity? (3) Mutation or MR or planted fail? (4) Are we padding Cover% without kill evidence? |
| **Stance** | **Embody** advisory mutation + metamorphic; **Refuse** Cover%/LLM-judge as structural proof; suite-wide mutmut merge gate **Defer**. |

### 2.5 `sensor-ledger-spec`

| Lens | Content |
| --- | --- |
| **Theory** | Watch presents gap *classes*; compact ledger is SoR of findings; human Specs; fixer ≠ watch tip (E-STK0). Prevents tip thrash and context bloat. |
| **Mathematics** | Finding as typed event \(g \in \{G1..G6,\ldots\}\); ledger append-only; Spec is discrete state transition — not continuous chat. |
| **Algorithms / DS** | Sensor functions \(s_i: Repo \rightarrow Finding^*\); dedupe by fingerprint; rotate focus; cycle reset. |
| **ETL** | Sensors write ledger markdown/JSON; backlog/Spec are derived views of approved findings — chat dumps **Refuse** as SoR (DOC12). |
| **Impl** | Finding ledger under `docs/research/findings/`; E-STK1 Deferred until Active + CGQ3. |
| **Traversal checklist** | (1) Is this an instance or a class? (2) Ledger entry id? (3) Spec before fix? (4) Watch tip ≠ fixer tip? |
| **Stance** | **Embody** sensors+ledger pattern; **Adopt** E-STK1 when Active; memory daemons **Refuse/Defer** per STK. |

---

## 3. Missing codegen-quality dimensions (preflight map)

Dimensions **not** yet enforced as generation preflight (post-hoc CI may touch some).

| Dimension | What it controls | Evidence | Repo today | Stance |
| --- | --- | --- | --- | --- |
| **Structural grounding** | Probe imports/public surface/callers before design | [2604.05278] discovery hooks | Partial ast-grep/tach; not required pre-Spec | **Adopt** probe→Spec recipe |
| **Spec information completeness** | Outcomes, bounds, constraints, priors, tasks, Verify | SDD practice; Spec Kit stages | Spec process exists; often thin Accept | **Adopt** CGQ3 template |
| **Independent verifier** | Check against Spec/evidence, not author narrative | [2604.05278] validation; generator≠verifier | Human + CI; no systematic adversarial Verify | **Adopt** process; LLM-judge **Refuse** as SoT |
| **Contract fidelity** | Only existing symbols; patch-at-use | Context blindness symptoms [2604.05278] | Embodied in hotfixes | **Embody** + preflight |
| **Effect / blast-radius map** | Observable effects + coupling before edit | Feathers effect analysis | Culture; not required | **Adopt** before reshape |
| **Spec↔witness traceability** | Accept ↔ test/fixture path | Claims `verify:` analog | Docs yes; design Accept weak | **Adopt** |
| **Context-bundle quality** | Bounded evidence pack vs chat lore | STK lean context; grounding hooks | Look-first hooks | **Adopt** with ledger |
| **Security / misuse surface** | Unsafe defaults, path/secret misuse in new code | [2605.09059] quality beyond correctness | Thin | **Adopt** selective sensors |
| **Dead / orphan surface** | Leftover exports after splits | Façade incidents | Partial | **Defer** fitness until Spec |
| **Change-risk / hotspots** | Churn × complexity × coupling | Ops quality dims (industry) | Unknown product gate | **Defer** / sensor |
| **Production reviewability** | Colleague-accept readability/maintainability | [2605.09059] human review | Soft culture | **Advisory** v1 |
| **Oracle richness (PBT)** | Property oracles | Hypothesis; E-QA | Deferred Spike | **Keep Defer** |

---

## 4. Spec Accept shape (load-bearing)

```text
Concern (optional DDIA id)
  → Remedy mechanism id (§2)
  → Depth-row cite (this memo §2.x or Explicit Defer + exit)
  → Witness path (test / fixture / gate that fails closed)
  → Independent Verify notes (what checks Spec, not the PR story)
```

Naming a remedy without a depth-row cite is **incomplete** (same class as DDIA-only Specs).

---

## 5. Spec decisions (CGQ1–CGQ10) — pending Approve

| ID | Decision |
| --- | --- |
| **CGQ1** | Pre-generation controls are first-class; post-hoc CI is necessary≠sufficient for agent codegen quality |
| **CGQ2** | Mechanism depth rows required before Embody of any **new** fitness / ETL / characterization net |
| **CGQ3** | Spec Accept template: Concern → Remedy id → Depth-row cite → Witness path → Explicit Defer if incomplete |
| **CGQ4** | Structural grounding probe (imports / public surface / callers) required for design-shaped Impl |
| **CGQ5** | Independent Verify step (gates + checklist against Spec, not author narrative); LLM-judge ≠ SoT |
| **CGQ6** | Amend E-SOL0: `effective-remedies` + page sections = **vocabulary** until depth Approve; SOL11 remains section-presence fitness only |
| **CGQ7** | E-COH1 / E-STK1 may become Active only with CGQ3 Accept rows |
| **CGQ8** | Refuse: Spec Kit WorkflowEngine runtime; Sonar/LLM-judge as floors; dual arch linters; raising constitution ceilings |
| **CGQ9** | ≥10k★ bar unchanged for new tool Adopts; Confirmed vehicles (pytest, tach, ast-grep, mutmut advisory) host mechanisms |
| **CGQ10** | Research memos for design-shaped work must include mechanism depth subsections or Explicit Defer with exit criterion |

---

## 6. Adversarial checklist

- [ ] Remedy named without §2 depth cite? — **Fail CGQ2.**
- [ ] Spec cites only DDIA or mechanism id? — **Fail CGQ3 / SOL1.**
- [ ] Design-shaped Impl without structural probe? — **Fail CGQ4.**
- [ ] Verify = “tests I wrote while generating” with no Spec checklist? — **Fail CGQ5.**
- [ ] New fitness coded before CGQ Approve? — **Fail** (this epic bound).
- [ ] Cover% or LLM-judge offered as structural/generation proof? — **Fail CGQ8.**

---

## 7. Epic sketch

### E-CGQ0 — Spec gate (this memo)

Exit: human Approve CGQ1–CGQ10; backlog P21.0 → Approved.

### Follow-ons (ordered, one Active)

| Epic | Uses | Notes |
| --- | --- | --- |
| **E-GND0** | CGQ4, CGQ5 | Tip-grounding MCP Spec ([`process/25`](25-tip-grounding-mcp-2026.md)); Implement after this epic Approve |
| **E-COH1** | CGQ3, CGQ4, characterization depth §2.3 | Reshape only with net + probe |
| **E-STK1** | CGQ3, §2.5, fitness depth §2.1 | G1–G6 sensors as fitness |
| **E-SOL0 Approve** | CGQ6 | Vocabulary + depth together |

---

## 8. Exit

**E-CGQ0 APPROVED** (2026-08-09, velocity stamp).
CGQ4 structural probe / CGQ5 independent Verify: **process + existing tools** until E-GND1.
Active Implement tip after Approve: **E-STK1** (not E-GND1).

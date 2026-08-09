---
status: SUPERSEDED — do not use as SoT
superseded_by:
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - docs/research/01-coverage-oracle-climb-solid.md
  - docs/research/02-foundational-agentic-se-2026.md
  - docs/research/03-scientific-dimensions-metrics.md
  - docs/research/04-implementation-frameworks.md
  - docs/research/05-dynamics-neuromorphic.md
date: 2026-08-08
note: Historical coordinator dump only. Merge complete on wave1 tip after 5eaac2a.
---

# WIP: coverage design audit (SUPERSEDED)

> **Superseded.** Read
> [`se-quality-synthesis-2026-08-08.md`](se-quality-synthesis-2026-08-08.md) and
> [`quality-backlog.md`](quality-backlog.md). Body below is archival dump only.

## A. Dual-mode oracle vs climb — prior audit (for segment 01)

### Seams `[Confirmed]`
- `src/doc_engine/ci/coverage_measure.py` — `MeasureRun` full-suite only; hardcodes `--cov=doc_engine --cov=stf`; applies `fail_under`
- `PathCohesionGuard` — single-writer / refuse foreign `wt-*` paths
- CONTRIBUTING: cov-only Python 3.11; gap-average = below-floor inventory; diff-cover = new-code gate
- Design memo: `docs/design/coverage-measure-modes-design-2026-08-08.md` status AWAITING CONFIRMATION

### Decisions already in design memo (1–16)
1–12 dual-mode design (entry point, scope, no climb fail_under, derived gap, cadence, PathCohesion, CI floor, xdist defer, diff-cover, thin CLI, banner, wave1 tip)
13 Strategy/polymorphism (`MeasureMode.ORACLE|CLIMB`) — not if/elif god
14 Naming bar — domain vocabulary; no `m`/`o`/`c`
15 complexipy ≤5 / no mode-boolean soup
16 DDIA SoT tightenings + promotion ban (climb artifact path product choice open)

### Principle scores (1–12 as a set) — coordinator draft
| Concern | Score |
| --- | --- |
| DDIA | Partial (need 16) |
| SOLID | Partial (need 13) |
| DRY | Partial (Metz: wrong abstraction risk) |
| OCP | Partial → 13 |
| Cyclomatic/cognitive | Gap → 15 |
| Naming | Gap → 14 |

### Key citations already verified `[Evidenced]`
- CoverUp arXiv:2403.16218 — iterate missing segments; final whole-suite check
- ChaCo arXiv:2601.10942 — patch-scoped ≠ whole-repo floor
- pytest-cov config — `--cov=PATH` overrides source; fail_under on **reported** total
- pytest-cov#528; DeepWiki pytest-cov CovController / xdist combine
- Kleppmann dual-writes blog + DDIA Part III SoR vs derived
- Martin OCP; Sandi Metz wrong abstraction; Campbell Cognitive Complexity; complexipy / CONTRIBUTING ≤5
- Naming: Clean Code; Hofmeister et al. (shorter IDs slower)

### Verdict draft
**Amend 13–16 before approve 1–12.** Not safe as-is.

---

## B. Foundational vs Agentic 2026 — source verification (for segment 02)

| Claimed | Result |
| --- | --- |
| arXiv:2606.04967 | **OK** — *From Prompt to Process…* Spec Kit / OpenSpec / Spec Kitty process taxonomy |
| arXiv:2608.03392 | **OK** — *Self-Evolving Coding Agents* survey; SICA/SIFT labels **Unknown** (not paper title objects); Gödel Machines = classic Schmidhuber |
| arXiv:2512.22256 | **OK** — *Agentic Software Issue Resolution…*; phases ≈ preprocess/localize/repair/validate/select |
| arXiv:2412.09284 | **OK** — log smells taxonomy (9 smells) |
| arXiv:2604.00787 | **OK** — MSR-LM survey / taxonomy |
| DeepWiki “crupig” | **Unknown** — not found; closest = langchain-ai/openevals LLM-as-Judge |
| DeepWiki “pierpaolo28” FDE | **Unknown** — not found |
| Thesirix cartography | Weak secondary profile mindmap only — vocabulary checklist, not product architecture |

### Stance draft (Embody / Adopt / Refuse)
- µsvc/EDA/CQRS/serverless as product infra → **Refuse**; CQRS-like oracle-write / gap-read analogy OK
- SDD (Spec Kit/OpenSpec) → **Adopt lightweight** one-stream Spec→Impl→Verify
- Self-evolving scaffolds ungated → **Refuse** (no CONSTRAINTS/baseline rewrite without human+claims)
- Issue-resolution workflow → **Embody partial**; Verify = deterministic gates
- LLM-as-judge → **Refuse as SoT**; advisory only
- FDE/enterprise RAG as core → **Unknown/refuse-as-core**
- MSR-LM → **Embody partial** (Stage-0 hermetic fixtures)

### Decisions draft already in taxonomy memo (17–24)
17 Layer binding oracle=SoT climb=feedback  
18 Bounded context + hexagonal strategies  
19 No ungated self-evolution  
20 LLM-judge ≠ fail_under  
21 SDD one-stream  
22 Framework refuse list (ECS, mesh, Backstage-required, GitOps controllers, WASM/Rust default)  
23 Green-Ops optional; keep cov-only-3.11  
24 Semantic density via names/modules; no SDE CI in v1  

Full draft lives in `docs/agentic-foundational-se-taxonomy-2026-08-08.md` — **de-dupe against sibling 02/04 when merging**.

---

## C. Scientific dimensions — notes (for segment 03)

### Structural & Cognitive
- McCabe cyclomatic classic; we gate **cognitive ≤5** via complexipy `[Confirmed]`
- Size ≤225 hard; soft advisory bands exist in CONTRIBUTING evidence table
- Semantic density: arXiv:2604.07502, 2604.17659 `[Evidenced]` — prefer descriptive names; refuse abbreviation theater

### Computational & Environmental
- Green AI Schwartz arXiv:1907.10597
- Already: cov-only-3.11 cuts matrix waste
- Climb = time/energy accelerator; not floor
- Rust/WASM: pick-none default (cross-link Rust memo)

### Architectural & Operational
- PathCohesion + single-writer = cohesion/SoT
- fail_under ≈ SLO-like hard floor
- Golden path = `doc-engine quality-gates` / coverage-measure / claims — not Backstage

### Agentic & Probabilistic
- Climb = verification-loop metric; oracle = acceptance
- Refuse LLM-judge as fail_under
- Recall@K formal gate = Unknown / out of v1

---

## D. Implementation frameworks — notes (for segment 04)

| Framework | Stance draft |
| --- | --- |
| DDD bounded contexts | Embody / deepen |
| Hexagonal ports for measure modes | Adopt |
| Vertical slicing vs type layers | Embody |
| DOD/ECS | **Refuse** |
| WASM/Rust hot paths | Refuse by default |
| Green-Ops / carbon CI | Optional later |
| Platform/IDP/Backstage | Embody golden-path CLIs; refuse Backstage install |
| GitOps Argo/Flux | Analogy only (git SoT for baselines); refuse controllers |
| Service mesh | **Refuse** |
| SDD/OpenSpec | Adopt process |
| Multi-agent orchestration | Refuse unordered parallel tip; OK only with single-writer+verify |
| RAG semantic index | Partial; never replace Stage-0 determinism |

---

## E. Dynamics / bio-inspired — coordinator notes (for segment 05) — incomplete

Research started; **do not treat as final** — sibling 05 is SoT when it lands.

### 1. Temporal coding & saliency
- Real domain: neuromorphic event cameras / SNN saliency (e.g. SpikeSlicer arXiv:2410.02249; AICAS/IJCNN event attention papers)
- Honest map to us: **metaphor only** → debounce / rate-limit agent remesure storms; climb batch cadence; anti CI event-storm
- **Refuse:** neuromorphic runtime, spike membranes, DVS pipelines in doc-engine
- **Adopt (engineering analogue):** saliency = “fire oracle remesure only on salient triggers” (batch end / pre-PR / empty inventory) — already in design decision 5

### 2. Gradient / fuzzy + hysteresis
- Real ops: alert flapping / hysteresis (Nagios flap detection; dual thresholds + dead band) `[Evidenced]` secondary SRE practice
- Continuous risk scores (e.g. FlexGuard) ≠ our coverage SoT
- **Embody:** size soft advisory vs hard >225; complexipy ratchet toward 0
- **Adopt:** hysteresis for *climb targeting thrash* / optional advisory bands near floor — e.g. don’t re-pick file every micro-delta
- **Refuse:** making oracle `fail_under=98.7` a fuzzy confidence; no gradient “confidence of green” replacing hard predicate

### 3. SoA vs AoS
- Wikipedia / architecture lit: SoA pays for SIMD/batch field scans; AoS for per-object random access
- **Refuse** SoA/DOD rewrite of `doc_engine` domain graphs
- When DOD pays: large homogeneous numeric scans (sim/games/GPU) — not AST/signal object graphs

### 4. PID / homeostatic
- Real: PID autoscaling for containers/microservices (e.g. arXiv:2109.02514; SHOWAR; cloud PID papers)
- **Refuse for v1** as coverage-floor controller
- **Optional later:** CI concurrency / rate caps with simple limits first; PID only if simple caps fail
- **Hard invariant:** oracle Cover% / fail_under stay **boolean predicates**, never PID error term that softens 98.7

### Draft decisions (pending sibling 05 confirmation) — proposed 25–28
25. **Hard predicates stay hard:** `fail_under` / oracle certified floor are boolean SoT; no PID/fuzzy softening.  
26. **Saliency for climb cadence:** rate-limit / debounce full oracle remesure; climb batches fire on salient triggers only (align decision 5).  
27. **Hysteresis allowed only on advisory bands / targeting:** size soft-band, climb “almost green” thrash control — never on oracle pass/fail.  
28. **SoA/neuromorphic/PID theater refused** for doc-engine domain models and coverage SoT.

---

## F. Merge plan (when parent resumes)

1. Wait until all five `docs/research/0N-*.md` exist.
2. Merge into `docs/research/se-quality-synthesis-2026-08-08.md`:
   - Source verification table
   - Per-layer scorecards
   - Unified decision list 1–N (reconcile taxonomy memo 17–24 + dynamics 25–28 + segment deltas)
   - Verdict on dual-mode approve
3. Write short `docs/research/quality-backlog.md` — Embody / Adopt / Refuse + ordered improvements.
4. Cross-link/update `docs/design/coverage-measure-modes-design-2026-08-08.md` verdict to point at synthesis.
5. Push wave1 **docs-only** if tip free of unrelated WIP; else report path.
6. **No dual-mode code implementation.**

## G. PARK

Coordinator parked. Next action only on parent resume after siblings land.

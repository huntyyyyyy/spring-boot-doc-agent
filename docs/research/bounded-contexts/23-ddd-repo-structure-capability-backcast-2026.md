---
title: E-REPO0 amend — future-capability backcast of repository structures
status: DRAFT Spec companion — pending Approve with memos 21+22 as one packet
research date: 2026-08-10
research_window: product SoT as of tip (STATUS / maturity / adoption / backlog)
claim tiers: Evidenced / Confirmed / Unknown
product: doc-engine — portable Spring-doc pipeline + adapters + meta quality monorepo
parent:
  - docs/research/bounded-contexts/21-ddd-repository-structure-options-2026.md
  - docs/research/bounded-contexts/22-ddd-repo-structure-quality-deepdive-2026.md
sources_of_future:
  - STATUS.md
  - MATURITY_ASSESSMENT.md
  - docs/product-architecture.md
  - docs/guides/principal-adoption.md
  - docs/adoption-hardening.md
  - docs/research/archive/claude-lore/research/adoption-blockers-queue-2026-07-30.md
  - docs/research/archive/claude-lore/10-architecture-maturation-plan.md (historical; §0–1 not executable)
  - docs/research/quality-backlog.md
  - CONSTRAINTS.md (enterprise gaps)
do_not:
  - invent a product vision not evidenced in the sources above
  - treat archived maturation Phase checklists as Active Spec
  - weaken fail_under 98.7 / complexipy ≤5 / LOC ≤225 / PathCohesion / 16-A
  - rank layouts without stating which horizon they optimize
spec_gate: DRAFT E-REPO0 amend (2026-08-10) — capability-backed possibilities; Approve with 21+22
---

# Future-capability backcast: solid structure possibilities

**Honest precondition.** Memos 21–22 ranked layouts from *present* smells and quality
research. This amend answers: *given what this project is supposed to become*, which
structures still win — with **pros/cons per possibility**, stress-tested against a
capability roadmap derived from in-repo SoT (not invented vision).

**Claim tiers:** `[Evidenced]` external · `[Confirmed]` in-repo SoT · `[Unknown]` open product choice.

---

## 0. One-page verdict (capability-aware)

| Question | Answer |
| --- | --- |
| Is there a single future-vision SoT? | **No.** Future is a **constellation**: STATUS “Next”, maturity adoption gates, principal-adoption brief, adoption-blockers residual queue, quality backlog, CONSTRAINTS enterprise close-out. `[Confirmed]` |
| Does that constellation change the spine? | **Partially.** Still refuse microservice/workspace bang and layer-first top. **Strengthen** H-pattern (more *bases*: CLI, Action, plugin, MCP, future HttpLLM), **K** (pipeline is the product), **J** (fact-store / certification / climb as truth classes), **I** (scanner SPI / multipass). |
| Best near-term package? | **Possibility 2** (deep BC packs + tach) **composed with** Possibility 3’s stage language for `tools/` and Possibility 4’s *logical* truth labels — then Possibility 5 only when a second installable/runtime base hurts. |
| What future feature would flip ranking? | **Multi-repo batch + RBAC as a first-class product** (CONSTRAINTS enterprise, lowest urgency today) → reconsider Possibility 8. **HttpLLM as default executor** → strengthen Possibility 5 bases. |

---

## 1. Capability roadmap (from repo SoT — not aspirational fiction)

### 1.1 Horizons

| Horizon | Intent | Sources |
| --- | --- | --- |
| **H0 — Now (locked)** | One portable CLI wheel; Path A/B; Claude generative adapter; GH Action; product tools under `doc_engine.tools`; meta in `scripts/`; query + MCP adapters; facts dual-emit Phase 1; certification as derived fold; quality constitution (98.7, size, complexipy, claims) | product-architecture, STATUS, E-CM/E-MOD |
| **H1 — Pilot hardening (next engineering)** | Documented mid-size Stage-4 `measured_stage4_inputs`; live Stages 1–4 once; semantic-eval on a real run; capacity on largest intended service; lineage dialect residual; L2 risk honesty | STATUS, adoption-hardening, adoption-blockers L2/L2b, maturity checklist |
| **H2 — Product deepen** | Richer fact-store beyond Phase 1 dual-emit (maturation **REFINE** thesis: addressable facts, contested maps); multipass/metamodel scanner registration; query/context-packet deepen; stalker agents (E-STK1); tach/cohesion modularity; optional CI semantic harness | maturation plan (directional), stage0 residuals, quality backlog P15–P17 |
| **H3 — Estate / enterprise (explicitly deferred)** | Branch protection (owner); deeper audit than run_manifest; **RBAC**; **multi-repo / batch**; Option C `HttpLLMStageExecutor` (named customer only); entry-point SPI | CONSTRAINTS enterprise, STATUS “Later / not now”, principal-adoption “Do not adopt yet” |

### 1.2 Capability → structure pressure

| ID | Capability | Structure must enable | Breaks if… |
| --- | --- | --- | --- |
| C1 | Portable one-wheel install | Single public package story | Many unpublished path deps become customer API |
| C2 | Path A deterministic + Path B generative | Clear kernel vs adapter boundary | Generative skills import kernel internals |
| C3 | Stage graph / `build_stage_specs` | Stage/tool code findable; ports for executors | Flat `tools/` InCol; mock/live/HttpLLM tangled |
| C4 | Scanner SPI + future multipass | Backend registry + deep scanning BC | New scanner = edit five grab-bags |
| C5 | Fact-store evolve (Phase 1+) | Encoding BC / schemas + scan emitters OCP | Facts schema edits scatter across tools |
| C6 | Certification / gates as derived views | Truth-class separation (SoR vs fold vs climb) | Climb/oracle/cert writers collocated casually |
| C7 | Capacity + Stage-4 scale | Partition/capacity cluster cohesion | Preflight logic split from partition/edges |
| C8 | Query + MCP | Query BC public façade; adapters thin | MCP reaches into pipeline guts |
| C9 | Drift + re-run (not continuous fleet) | Drift tool beside Stage-0 signatures | “Platform services” folder implying always-on |
| C10 | Multi-deployable: CLI, Action, plugin, MCP | Shared components, distinct bases | Copy-paste across adapters |
| C11 | Agent/skills DX + stalkers | Context packs / skill↔BC map | Agents load whole monorepo to change one gate |
| C12 | Meta quality (claims, rule coverage) | Meta ≠ wheel | `scripts/` absorbed into installable package |
| C13 | (H3) Multi-repo batch / RBAC | Orchestration boundary outside single-repo CLI | Premature platform monorepo now |
| C14 | (H3) HttpLLM executor | `StageExecutor` port + new adapter base | Executor buried in `local_runner` god module |

**Explicit non-goals that constrain structure** `[Confirmed]`: unattended fleet day-one; Backstage/mesh; packaging mega-PR restart; Spec Kit WorkflowEngine runtime; utils bags.

---

## 2. Solid possibilities (pros / cons vs roadmap)

Each possibility is a **coherent package** (not a single folder trick). Scoring uses H0–H3.

Legend for horizon fit: **Strong** / **OK** / **Weak** / **Hostile**.

---

### Possibility 1 — Logical overlay only (DOMAIN_MAP + truth labels + markers)

**Sketch.** Keep filesystem. Add `DOMAIN_MAP.md` / CODEOWNERS / pytest domain markers / truth-class labels (SoR | derived | sensor | product | meta | adapter).

| Horizon | Fit |
| --- | --- |
| H0–H1 | **Strong** (zero churn while pilots run) |
| H2 | **OK** until packs outgrow map |
| H3 | **Weak** (doesn’t create batch/RBAC seams) |

**Pros**
- Matches “packaging paused”; PathCohesion / claims safe.
- Immediately teaches C6/C12 (truth + meta) without `git mv`.
- Unblocks PairSmell inventory and E-TEST alignment.
- Lowest risk while H1 calibration runs (live Stage-4, semantic eval).

**Cons**
- Does not shrink `tools/` InCol — smell remains.
- Agents still pay full-tree context (hurts C11).
- Easy to ignore; map drifts unless claims-gated.
- Does not prepare C10 multi-base assembly.

**Verdict:** **Adopt as Wave 0 mandatory**; not a destination.

---

### Possibility 2 — Vertical deep BC packs + tach interfaces (A+F+O)

**Sketch.** `pipeline/`, `scanning/`, `query/`, `compliance/`, `ci_sensors/`, thin `cli/`; each deep pack = narrow façade + `lib/`/`internal/`; tach `depends_on` + `[[interfaces]]`; dissolve `tools/` into BCs.

| Horizon | Fit |
| --- | --- |
| H0 | **Strong** (C1–C4, C8) |
| H1 | **Strong** (capacity/partition land in one BC) |
| H2 | **Strong** (fact emitters OCP inside scanning; stalker sensors beside ci) |
| H3 | **OK** (HttpLLM as adapter calling ports; batch still external) |

**Pros**
- Aligns locked product-architecture + E-MOD/E-TACH.
- Best default for C1 portable wheel.
- Deep modules cut shallow fan-out; fitness in CI.
- Natural home for C4 scanner SPI and C8 query façade.
- Supports C14 via `StageExecutor` port without new top taxonomy.

**Cons**
- Large strangler cost inside `tools/` (62 modules).
- Does not by itself scream product at repo root (C11 partial).
- Truth-class (C6) still easy to violate inside `ci_sensors/` unless labeled.
- Multi-deployable sharing (C10) stays informal (imports across adapters).

**Verdict:** **Primary Implement spine** after Wave 0.

---

### Possibility 3 — Stage-DAG dissolution language (K under BC names)

**Sketch.** While executing Possibility 2, name/move tool clusters as stages: `s0_signals`, `s1_partition_capacity`, `s4_gates_cert`, registry stays `build_stage_specs()`.

| Horizon | Fit |
| --- | --- |
| H0–H2 | **Strong** for C3/C7 |
| H3 | **OK** |

**Pros**
- Ubiquitous language matches the actual product (a pipeline).
- Directly attacks measured clusters (partition≈28, scan≈18, gates≈10).
- Helps H1 Stage-4 work: capacity/partition co-located.
- New generative ports (mock / live / HttpLLM) hang off stage boundaries cleanly (C14).

**Cons**
- Temporal decomposition risk (Ousterhout): shared “dataset” concepts can split badly if stages ≠ BCs.
- Two taxonomies (stage vs BC) confuse unless stages *are* the BC names or nest under one BC.
- Overfit if product later becomes more “library of scanners” than staged pipeline.

**Verdict:** **Adopt as dissolution dialect inside Possibility 2**, not a parallel forever taxonomy.

---

### Possibility 4 — Truth-class zones (J): SoR / derived / sensor

**Sketch.** Logical first (labels); optional later physical `truth/{sor,derived,sensors}` for coverage writers, certification fold, climb, adequacy, stalker ledger.

| Horizon | Fit |
| --- | --- |
| H0 | **Strong** for C6 (certification already derived fold) |
| H1–H2 | **Strong** (climb ≠ oracle; adequacy sensors; fact-store SoR) |
| H3 | **OK** |

**Pros**
- Encodes policy **16-A** and DDIA SoR vs derived in navigation — unique to *this* product’s quality spine.
- Prevents H2 fact-store work from dual-writing climb/oracle/cert paths.
- Stalker agents (C11/E-STK) get an obvious “sensor” shelf that cannot claim floor.

**Cons**
- Unusual; onboarding cost for contributors expecting `src/` only.
- Physical move collides with coverage PathCohesion / CI paths — high blast radius.
- Over-partition if every script gets a truth label without need.

**Verdict:** **Adopt logical immediately**; physical only if REPO-S4 shows overlay failure.

---

### Possibility 5 — Multi-base component assembly (Polylith *pattern*, not polylith-cli)

**Sketch.** Conceptual `components/*` shared; `bases`: `cli`, `github_action`, `claude_plugin`, `mcp_server`, future `http_llm_executor`; `projects` assemble wheel vs marketplace pack.

| Horizon | Fit |
| --- | --- |
| H0 | **OK** (already have adapters; pattern clarifies) |
| H1 | **OK** |
| H2 | **Strong** for C10/C11 |
| H3 | **Strong** if HttpLLM / more adapters arrive |

**Pros**
- Best answer to C10: CLI + Action + plugin + MCP without publishing internal libs.
- H3 HttpLLM becomes another **base**, not a tumor in `local_runner` (C14).
- Agent DX: one development view over bricks (Polylith docs claim) — helps C11.
- Keeps customer wheel thin (C1) if projects declare brick sets explicitly.

**Cons**
- Conceptual overhead while only one primary runtime matters for pilots (H1).
- polylith-cli &lt;1k★ — must implement with setuptools/tach, not new SoR tool.
- Mis-applied → fake microservices / many pyprojects (Possibility 8 creep).
- Does not fix InCol inside components by itself.

**Verdict:** **Adopt pattern docs + REPO-S5 sketch in H1**; physical bases/ folder **Defer** until a fourth base hurts or HttpLLM is scheduled.

---

### Possibility 6 — Hive: mini-hexagon per hot BC (I)

**Sketch.** Especially `scanning/` and `pipeline/`: local `domain|application|ports|adapters`.

| Horizon | Fit |
| --- | --- |
| H2 | **Strong** for C4 multipass / metamodel adapters |
| H3 | **Strong** for SPI swaps |
| H0–H1 | **OK** (heavy for pilot hardening) |

**Pros**
- New scanner backend = new adapter; core untouched (OCP) — matches maturation SOLID notes.
- Clean extraction story if a scanner later becomes its own distribute (without committing to µsvc).
- Aligns E-MOD hexagonal without global `domain/` bag (memo 21 Refuse E).

**Cons**
- Nesting tax; fights LOC≤225 if applied ceremonially everywhere.
- Wrong default for thin BCs (query handlers may not need full hexagon).
- Contributors may recreate layer-first *inside* every folder.

**Verdict:** **Adopt only in scanning (and maybe pipeline executor)** when multipass/SPI work starts; not repo-wide.

---

### Possibility 7 — Agent-context packs (M)

**Sketch.** Map (then optionally colocate) `stage0`, `certification`, `query`, `meta-claims`, each with src + tests + skills + fixtures pointers.

| Horizon | Fit |
| --- | --- |
| H1–H2 | **Strong** for C11, semantic-eval skill, stalkers |
| H0 | **OK** as maps |
| H3 | **OK** |

**Pros**
- Directly reduces agent context load — Polylith’s agent-DX insight without the tool.
- Skills stop floating detached from the BC they invoke (C2/C11).
- Supports E-STK rotating focus (one pack per watch domain).

**Cons**
- Physical colocation can break marketplace plugin packaging / skill mirror CI.
- Risk of duplicating trees (`adapters/claude/skills` vs packs).
- Over-packaging small concerns.

**Verdict:** **Adopt as maps in DOMAIN_MAP**; physical colocation only with adapter packaging spike.

---

### Possibility 8 — Multi-package workspace / publishable libs (C from memo 21)

**Sketch.** uv/poetry workspace; `packages/doc-engine-*`; apps compose.

| Horizon | Fit |
| --- | --- |
| H0–H2 | **Weak / Hostile** to C1 simple install |
| H3 | **OK→Strong** *only if* multi-repo batch becomes a distributed product |

**Pros**
- Hard package boundaries; independent versioning.
- Could host a future “fleet orchestrator” package beside CLI.

**Cons**
- Fights principal-adoption “pip install one wheel.”
- Massive claims/CI churn; premature for deferred RBAC/multi-repo.
- Encourages library sprawl before fact-store deepen.

**Verdict:** **Defer until H3 multi-repo is an approved product bet** — not before.

---

### Possibility 9 — Screaming capability root (G) ± physical product/meta/policy (B)

**Sketch.** Root names `document-spring/`, `meta-quality/`, `agent-policy/` (physical or mapped).

| Horizon | Fit |
| --- | --- |
| H0–H1 | **OK** (map) / **Weak** (physical during pilots) |
| H2–H3 | **OK** for onboarding orgs |

**Pros**
- Fixes scream test; helps external adopters (principal brief audience).
- Makes C12 meta boundary obvious.

**Cons**
- Physical root move = hooks, Action, plugin, Cloud agent path blast.
- Does not fix internal `tools/` InCol alone.
- Cosmetic if map already screams.

**Verdict:** **Adopt scream names in DOMAIN_MAP now**; physical root **Defer** (REPO-S1).

---

### Possibility 10 — Explicit refuse set (still listed for completeness)

| Layout | Why refuse for *this* future |
| --- | --- |
| Layer-first top (`domain/application/infra`) | Wrong ubiquitous language; harms C3/C4; E-MOD M4 |
| Colocated domains bang (`domains/*/src+tests`) | Breaks H1 PathCohesion / claims during pilot hardening |
| DDIA-domain-named packages | Design catalog ≠ Spring-doc language |
| ArchAgent LLM recovery as structure SoT | Non-deterministic; H2 fact-store needs human Spec |
| Always-on platform / fleet folders | Contradicts “no unattended fleet”; C9 is deliberate re-run |

---

## 3. Cross-matrix: possibility × critical capabilities

| Possibility | C1 wheel | C3 stages | C4 scanners | C6 truth | C10 bases | C11 agents | C13 batch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Overlay | ✓ | ~ | ~ | ✓ label | ~ | ~ | ✗ |
| 2 Deep BC+tach | ✓✓ | ✓ | ✓✓ | ~ | ~ | ✓ | ~ |
| 3 Stage-DAG dialect | ✓ | ✓✓ | ✓ | ~ | ~ | ✓ | ~ |
| 4 Truth zones | ✓ | ~ | ~ | ✓✓ | ~ | ✓ | ~ |
| 5 Multi-base pattern | ✓ | ✓ | ✓ | ~ | ✓✓ | ✓✓ | ~ |
| 6 Hive hot BC | ✓ | ✓ | ✓✓ | ~ | ~ | ~ | ~ |
| 7 Agent packs | ✓ | ✓ | ~ | ✓ | ✓ | ✓✓ | ~ |
| 8 Workspace pkgs | ✗ now | ~ | ✓ | ~ | ✓ | ~ | ✓ later |
| 9 Screaming root | ✓ | ~ | ~ | ✓ | ~ | ✓ | ~ |

---

## 4. Recommended composition (feature-backcast)

```text
Wave 0 (H0/H1, now):     Possibility 1 + logical 4 + scream names (9 as map)
Wave 1 (H1→H2):          Possibility 2 spine + Possibility 3 dissolution of tools/
Wave 1b (parallel docs): Possibility 5 pattern sketch (REPO-S5); Possibility 7 maps
Wave 2 (H2 scanners):    Possibility 6 inside scanning when multipass/SPI starts
Wave 2b (optional):      Physical 4 if overlay fails (REPO-S4)
Wave 3 (only if H3 bet): Possibility 5 physical bases/ and/or Possibility 8
```

**Do not** start Possibility 8 or physical root B to “get ready for RBAC.” Principal-adoption and CONSTRAINTS place multi-repo/RBAC last; structure prep that burns PathCohesion during Stage-4 calibration is negative EV.

---

## 5. Spec deltas (add to E-REPO0 Approve)

| ID | Decision | Stance |
| --- | --- | --- |
| **REPO17** | Structure Approve must cite capability horizons H0–H3 from this memo | **Embody** |
| **REPO18** | Optimize Wave 1 for H1 pilot hardening + C1–C8; not H3 estate | **Adopt** |
| **REPO19** | Schedule Possibility 5 pattern sketch before HttpLLM / extra bases land | **Adopt** |
| **REPO20** | Forbid Possibility 8 until multi-repo/batch is an Approved product Spec | **Refuse until** |

---

## 6. Adversarial checklist

- [ ] Did we invent fleet/RBAC urgency? — **No**; sources say lowest urgency / do not adopt yet.
- [ ] Does Stage-DAG fight fact-store? — Fact schema lives in encoding/scanning BC; stages *emit* facts, don’t own the schema forever.
- [ ] Does multi-base imply microservices? — **No**; in-process bases fine.
- [ ] Is STATUS stale vs backlog? — STATUS “Next” still points at Stage-4 / lineage; backlog Active is E-COH1 — structure must not thrash Active tip. `[Confirmed]` tension: note in Approve.
- [ ] Could H1 live runs be blocked by mass moves? — **Yes** → Wave 0 overlay first is mandatory.

---

## 7. Epic note

E-REPO0 Approve packet = **21 + 22 + this 23**.  
E-REPO1 Implement follows §4 composition; first ticket remains DOMAIN_MAP + truth labels + REPO-S3 inventory — **no** workspace migration.

**Exit for this amend:** human can pick a possibility set with eyes open on H0–H3 tradeoffs; rankings are no longer present-smell-only.

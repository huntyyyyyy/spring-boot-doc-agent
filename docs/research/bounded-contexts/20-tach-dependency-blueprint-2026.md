---
title: E-TACH0 — Dependency-map-as-blueprint (modern enforcement, Jun–Aug 2026)
status: DRAFT Spec — pending Approve of TACH1–TACH10
date: '2026-08-09'
research_window: 2026-06-01 → 2026-08-09
claim_tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`) — tach already cycle-gates;
  finer map Spec-gated
related:
- tach.toml
- docs/research/process/15-legacy-size-remediation-2026-frameworks.md
- docs/research/bounded-contexts/12-pipeline-stage0-modularity-ports-2026.md
- docs/research/bounded-contexts/16-scan1-astgrep-modularity-2026.md
- docs/research/se-quality-synthesis-2026-08-08.md
- CONTRIBUTING.md
do_not:
- expand tach.toml with depends_on while pipeline↔scanning / tools crosstalk cycles
  remain
- treat `tach sync` output as Approved architecture without human Spec
- dual-wire import-linter + tach without an explicit dual-gate Spec (LEG-S1)
- adopt pytestarch / grimp as merge SoR under the ≥1k★ bar
- use grab-bag utils/ to “pass” size ceilings
- copy Spring Modulith / Nx / Packwerk runtimes into this Python CLI
spec_gate: DRAFT E-TACH0 (2026-08-09) — TACH1–TACH10 pending Approve
gh_sor_bar: ≥1000★ and pushed_at within research_window (prefer Releases/CHANGELOG)
last_reviewed: '2026-08-10'
---

# Principal memo: dependencies as the repository blueprint (Jun–Aug 2026)

**Question.** How should this repo structure modules so dependency rules are the primary architectural SoR — without poorly re-implementing mid-2026 practice?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

**Research window:** 2026-06-01 → 2026-08-09. GitHub implement SoR: **≥1000★** and **`pushed_at` in window** (same bar as E-STK0). Star/push alone never imply Adopt — discernment §5 required.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is “dependency map as blueprint” the 2026 consensus for modular monoliths? | **Yes.** Industry + tooling treat **enforced** module edges (not folder convention) as the difference between modular monolith and ball-of-mud. `[Evidenced]` tach docs; ArchUnit/Modulith pattern literature; arXiv architecture-governance review [2607.26110](https://arxiv.org/abs/2607.26110) |
| Best **Python** primary enforcer for *this* product? | **Embody tach cycles** as **Confirmed pin** (already `~=0.35.0`). Under the raised **≥10k★** stream bar (E-STACK0 / HOT13), tach (~2.8k) is **not** external ★ SoR — re-base *new* boundary Spec on **Nx-class patterns** (≥29k★) + Confirmed vehicle; do not expand `depends_on`/`[[interfaces]]` from tach★ alone. `[Evidenced]` + `[Confirmed]` |
| Import-linter / PyTestArch / Packwerk / Nx? | **import-linter:** Spike/Defer dual-gate (meets ★+push; contracts overlap tach). **PyTestArch/grimp:** Refuse as implement SoR (&lt;1k★). **Packwerk/Nx/Spring Modulith:** Adopt *patterns* only (wrong runtime). `[Evidenced]` |
| Poor-implementation traps? | (1) `tach sync` as silent architecture, (2) `depends_on` before breaking real cycles, (3) modules without **interfaces**, (4) dual fitness tools without Spec, (5) LOC chops that ignore intended edges. |
| What to do on this tip before Approve? | Keep cycle gate; structure LOC/statement splits as **façades + future BC paths**; do **not** edit `tach.toml` module map until TACH Approve + cycle cleanup. `[Confirmed]` |

---

## 1. Problem frame (this product)

We already refuse forever-grandfather of size debt (E-LEG0) and split along DDD BCs (E-MOD*, E-SCAN1). User direction: **dependencies are the primary structuring mechanism** — tach-style declared imports, public surfaces, acyclic graph — not discipline or PR review hope.

Category errors to refuse up front:

| Error | Why |
| --- | --- |
| Folder rename = modular monolith | Without CI fitness, boundaries erode under deadline pressure |
| `tach sync` → commit = architecture | Sync *measures* reality; Spec *declares* intent (TACH7) |
| Dual import-linter + tach tomorrow | Overlapping predicates; LEG-S1 / FAC4 Defer dual gates |
| Spring Modulith / Nx as Python deps | Wrong ecosystem; steal patterns only |
| LLM architecture recovery as merge SoR | SemRef-class papers are sensors; gates stay deterministic |

---

## 2. Inventory (Jun–Aug 2026 window)

### 2.1 GitHub / docs SoR (primary)

| Candidate | ★ (2026-08-09) | `pushed_at` in window? | Latest relevant signal | Role |
| --- | --- | --- | --- | --- |
| **[tach-org/tach](https://github.com/tach-org/tach)** | **2786** | **Yes** (2026-06-11) | PyPI **0.35.0** (2026-05-12); tip commits 2026-06-11; docs: layers, interfaces, deprecate, unchecked modules, `tach map` | **Primary Python enforcer** |
| **[seddonym/import-linter](https://github.com/seddonym/import-linter)** | **1130** | **Yes** (2026-08-07) | **v2.13** (2026-07-03); contracts: forbidden / layers / independence / acyclic siblings | Alternate fitness / dual-gate Spike |
| **[Shopify/packwerk](https://github.com/Shopify/packwerk)** | **1900** | **Yes** (2026-07-27) | Ruby pack boundaries + public API | Pattern only |
| **[nrwl/nx](https://github.com/nrwl/nx)** | **29206** | **Yes** (2026-08-07) | Module boundary tags / enforce-module-boundaries | Pattern only (TS monorepo) |
| **python-grimp/grimp** | **128** | Yes (2026-08-07) | Graph library under import-linter | **Refuse** implement SoR (&lt;1k★) |
| **zyskarch/pytestarch** | **169** | Yes (2026-08-07) | ArchUnit-style pytest rules; blog 2026 “fitness functions” | **Refuse** implement SoR (&lt;1k★); pattern OK |

`[Evidenced]` via GitHub API + project docs on research date.

### 2.2 Tach capabilities that matter for a good implement (not just cycles)

From [tach docs](https://docs.gauge.sh/) / DeepWiki cartography `[Evidenced]`:

| Mechanism | What it prevents | Relevance here |
| --- | --- | --- |
| **`depends_on`** | Undeclared cross-module imports | BC map after cycles cleared |
| **`[[interfaces]]` `expose`** | Deep imports into internals | Façade discipline (E-MOD/E-SCAN) |
| **`layers` (+ optional closed / `layers_explicit_depends_on`)** | Upward imports; optional “no skip tier” | **Incremental** path before full edge list |
| **`forbid_circular_dependencies`** | Cycles | Already Embody in `tach.toml` |
| **Unchecked / incremental modules** | Big-bang rewrite | Adopt for rollout |
| **`tach sync` / `tach map`** | — | **Propose only**; human Approves blueprint |
| **Deprecate dependency** | Soft-fail while removing edge | Migration aid |

Pinned here: `tach~=0.35.0` (`requirements-dev.txt`). `[Confirmed]`

### 2.3 This repo today `[Confirmed]`

```toml
# tach.toml (abridged)
source_roots = ["src"]
forbid_circular_dependencies = true
[[modules]] path = "doc_engine"
[[modules]] path = "stf"
# no depends_on, layers, or interfaces
```

Measured mutual edges (naïve BC split would fail): `pipeline`↔`scanning`; `tools` fans into `pipeline`/`query`/`scanning`. SCAN1-H / LEG7 already **Defer** tach config refinement.

### 2.4 arXiv (window) — governance signal, not tool SoR

| Paper | Date | Use |
| --- | --- | --- |
| [2607.26110](https://arxiv.org/abs/2607.26110) architecture literature review | 2026-07-28 | Supports **continuous architectural governance** + DDD decomposition — aligns with CI fitness, not chat review |
| [2607.23774](https://arxiv.org/abs/2607.23774) SemRef (LLM + deps for architecture recovery) | 2026-07 | **Sensor / Spike only** — refuse LLM recovery as merge SoT |
| [2606.05720](https://arxiv.org/abs/2606.05720) MicroSkill modular knowledge | 2026-06-04 | Adjacent to context-lean agents (E-STK); not tach substitute |

---

## 3. How mid-2026 systems avoid poor implementation

| Practice | Source | Anti-pattern we refuse |
| --- | --- | --- |
| Declare **intent** then enforce | tach `depends_on` / layers docs | Sync-driven toml churn |
| **Public interface** for cross-module calls | tach interfaces; Packwerk public API; Modulith API packages | Re-export entire package as “façade” |
| **Layers first**, edges later | tach layers (0.33+ `layers_explicit_depends_on`) | Instant full BC matrix on cyclic code |
| **Fitness in CI** | tach check; ArchUnit/PyTestArch essays 2026 | Soft “please don’t import that” |
| **One primary enforcer** | CONTRIBUTING / LEG-S1 | Parallel IL + tach + pytestarch predicates |
| Break **cycles via ports** before stricter map | E-MOD ports; measured pipeline↔scanning | Raising baselines / ignore comments forever |

---

## 4. Deep adoption discernment (candidate → stance)

| Candidate | Solves | Coupling | Stance | One-line why |
| --- | --- | --- | --- | --- |
| **tach cycle gate** (current) | Acyclic `doc_engine`↔`stf` | Already CI | **Embody** | Boolean SoT we already ship |
| **tach layers** for BCs | Directional architecture without full edge list | `tach.toml` only | **Adopt** (first Implement wave after Approve) | Matches incremental docs; softer onboarding than full `depends_on` |
| **tach `depends_on` + interfaces** | Explicit blueprint + hide internals | Requires cycle cleanup + façades | **Adopt** (second wave) | User’s primary mechanism; needs green graph first |
| **`layers_explicit_depends_on` / closed layers** | No silent lower-layer reach-through | Stricter toml | **Spike** | Useful after layers stabilize |
| **import-linter contracts** | Layers/forbidden/independence | Second config language | **Defer** dual-gate | Meets ★+push; overlaps tach — LEG-S1 only |
| **PyTestArch fitness tests** | ArchUnit-style pytest | Test dependency | **Refuse** SoR (&lt;1k★) | Pattern OK inside a Spike, not merge gate |
| **grimp alone** | Import graph API | Lib | **Refuse** SoR (&lt;1k★) | Prefer tach / IL stacks |
| **Packwerk / Nx / Spring Modulith** | Packs / tags / modules | Wrong runtime | **Embody pattern / Refuse dep** | Public API + enforce-in-CI lessons only |
| **SemRef / LLM recovery** | Suggest module cuts | Non-deterministic | **Refuse** as SoT | May draft research questions only |

**Ranking for this Python CLI:**

1. Embody tach cycles (done)  
2. Adopt layered BC map → then `depends_on` + interfaces  
3. Defer import-linter dual gate  
4. Refuse &lt;1k★ pytestarch/grimp as gates; refuse foreign runtimes  

---

## 5. Spec decisions (TACH1–TACH10) — pending Approve

| ID | Decision |
| --- | --- |
| **TACH1** | Dependency rules are a **primary** structuring mechanism alongside LOC≤225 / statements≤20 / complexipy≤5 |
| **TACH2** | **tach** remains the sole production dependency fitness tool until a dual-gate Spec (LEG-S1) Approves otherwise |
| **TACH3** | Finer modules follow **domain BCs** (`scanning`, `pipeline`, `query`, `ci`, `tools`, `core`, `paths`, …) — not LOC folders |
| **TACH4** | Implement order: **(a)** break measured BC cycles via façades/ports, **(b)** introduce **`layers`**, **(c)** add **`depends_on` + `[[interfaces]]`**, **(d)** same-commit green `tach check` |
| **TACH5** | Cross-BC imports must use **declared public interfaces** (tach `expose` / package façade) — not deep internals |
| **TACH6** | `tach sync` / `tach map` may **propose**; humans **Approve** the blueprint in research/backlog — never silent architecture |
| **TACH7** | Inline `tach-ignore` / deprecated edges are **time-boxed debt**, not permanent policy |
| **TACH8** | Tests stay outside tach `source_roots` enforcement (current exclude); production `src/` is the SoR |
| **TACH9** | Refuse: utils bags, dual IL+tach without Spec, pytestarch/grimp as CI SoR, Modulith/Nx/Packwerk as runtime deps |
| **TACH10** | Size/statement remediation on Active tips must **respect future BC edges** even before toml lands (Adopt process now) |

---

## 6. Epic sketch (fresh-chat ready)

### E-TACH0 — Spec gate
- **Goal:** Approve TACH1–TACH10.  
- **Exit:** `spec_gate: APPROVED E-TACH0` + backlog P16.0 Approved.  
- **Non-goal:** Editing `tach.toml` module map.

### E-TACH1 — Cycle-break + layers (Implement)
| ID | Title | Acceptance |
| --- | --- | --- |
| TACH1-1 | Eliminate `pipeline`↔`scanning` mutual imports via ports/façades | `tach map` / import inventory shows one-way edge |
| TACH1-2 | Collapse illegitimate `tools` fan-in behind façades | tools depend only on allowed lower layer |
| TACH1-3 | Add `layers = [...]` + assign BC modules | `tach check` green; no upward imports |
| TACH1-4 | Document layer diagram in CONTRIBUTING | claims paths resolve |

### E-TACH2 — Explicit depends_on + interfaces
| ID | Title | Acceptance |
| --- | --- | --- |
| TACH2-1 | `depends_on` lists per BC module | undeclared import fails CI |
| TACH2-2 | `[[interfaces]]` for each BC façade | deep import fails CI |
| TACH2-3 | Optional Spike: closed layer / `layers_explicit_depends_on` | spike memo + yes/no |

**Invariants:** fail_under 98.7; complexipy ≤5; LOC ≤225; no utils/; one tip writer.

**Spikes:** TACH-S1 closed layers; TACH-S2 import-linter dual-gate (default **no**).

---

## 7. Adversarial checklist

- [ ] Does Approve allow editing toml before cycles are gone? — **No (TACH4).**
- [ ] Can agents treat sync output as Spec? — **No (TACH6).**
- [ ] Do we add pytestarch because a 2026 blog likes ArchUnit? — **No (&lt;1k★ + TACH2).**
- [ ] Does layer skip recreate deep coupling? — Spike closed layers (TACH-S1).
- [ ] Will ignores accumulate forever? — TACH7 time-box.
- [ ] Does this reopen forever-grandfather of LOC debt? — **No**; E-LEG still pays down; edges guide *how* we split.

---

## 8. Exit / next

- **Design pass (Active):** **E-COH0** — cohesion bar before more size thrash ([`docs/design/concept-split-cohesion-design-2026-08-09.md`](../../design/concept-split-cohesion-design-2026-08-09.md)).
- **Human:** Approve **E-TACH0** (TACH1–TACH10) and/or **E-COH0** (COH1–COH12).
- **Later:** E-COH1 reshape provisional modules → E-TACH1 layers → E-TACH2 depends_on+interfaces.
- Tip MOD-S1 concept splits are **provisional** (COH9) — not “Done modularity.”

DeepWiki used as **cartography only** for tach internals; merge decisions cite GitHub/docs/arXiv + this repo.

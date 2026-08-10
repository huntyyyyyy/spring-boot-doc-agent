---
title: E-REPO0 — DDD repository structure options (shallow root + fat folders)
status: DRAFT Spec — options inventory; pending Approve of REPO1–REPO16 (see companion 22)
research date: 2026-08-10
research_window: 2026-01-01 → 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`) + meta CI/adapters monorepo
related:
  - docs/research/modularity/22-ddd-repo-structure-quality-deepdive-2026.md
  - docs/product-architecture.md
  - docs/research/modularity/12-pipeline-stage0-modularity-ports-2026.md
  - docs/research/modularity/06-test-suite-bounded-contexts-parallel.md
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/design/ddia-north-star/domains/05-maintainability-and-change/
  - tach.toml
do_not:
  - big-bang git-mv of tests/ or src/ without Spec Approve + claims rewiring
  - treat folder rename as modularity (enforce with tach / markers)
  - introduce utils/ grab-bags or DI containers
  - adopt Nx / Packwerk / Spring Modulith / Backstage as Python runtimes
  - weaken fail_under 98.7, complexipy ≤5, LOC ≤225
  - cross-job coverage combine or PathCohesion breaks while reshaping tests
spec_gate: DRAFT E-REPO0 (2026-08-10) — REPO1–REPO20 pending Approve (21+22+23 packet)
gh_sor_bar: "≥1000★ and pushed_at within research_window (prefer Releases/docs)"
---

# Principal memo: at least five DDD-shaped repository structures

**Question.** The repo root is shallow and several subtrees fan out into many
siblings (tools, tests, support). How should we *organize* the tree with
strategic DDD (bounded contexts + enforced edges) — without poorly copying
2026 monorepo fashion?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

**Non-goal this tip:** implement any mass move. This memo drafts **≥5 distinct
layouts**, ranks them for *this* product, and Spec-gates a preferred path.

**Deep companions (required read for Approve):**  
- [`22-ddd-repo-structure-quality-deepdive-2026.md`](22-ddd-repo-structure-quality-deepdive-2026.md) — quality axes + unusual G–P  
- [`23-ddd-repo-structure-capability-backcast-2026.md`](23-ddd-repo-structure-capability-backcast-2026.md) — **future-capability roadmap + solid possibilities with pros/cons**  

**E-REPO0 Approve = memos 21 + 22 + 23 together.**

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is “shallow root + fat mid folders” a real problem here? | **Yes — but as quality smells**, not depth taste. Root fails the scream test; `tools/` is InCol; tests risk InSep; SoR/derived is not named in the tree. See companion §1. `[Confirmed]` + `[Evidenced]` |
| Is folder depth the fix? | **No.** Depth without **enforced** BC edges is DDD cosplay. `[Evidenced]` DDD 2026 practice; Packwerk/tach literature; E-TACH0 |
| Best fit for this CLI monorepo? | **A+F+O spine** (vertical BCs + tach packs + deep façades), with **N** logical overlay first; selective **J/K/H-pattern/I/M** from companion. `[Confirmed]` + companion §5 |
| Multi-package workspace / colocated domains / layer-first Clean Architecture? | **Defer** workspace; **Refuse** big-bang colocated slice move and layer-first top packages. |
| First Implement after Approve? | DOMAIN_MAP + truth labels + PairSmell inventory (REPO-S3) → façades — **not** root rename theater. |

---

## 1. Problem frame `[Confirmed]`

### 1.1 Measured hotspots (2026-08-10 tip)

| Location | Fan-out | Why it hurts |
| --- | --- | --- |
| Repo root | **27** top entries (`src`, `scripts`, `adapters`, `skills`, `spring-signals`, `claude`, …) | Product vs meta vs agent-policy mixed; navigation is flat, not domain-shaped |
| `src/doc_engine/tools/` | **63** top-level `.py` | Stage-0 / gates / validators share one grab-bag package — violates “concept-named modules” |
| `src/doc_engine/{pipeline,scanning,ci,query}` | 13–29 children each | Partially sliced; still uneven |
| `tests/doc_engine/` | **208** `test_*.py` (mostly flat) | Cohesion only via *filename prefixes* (`coverage_climb_*`, …) — E-TEST0 debt |
| `tests/support/` | **22** sibling packages | Meta helpers without product BC alignment |
| `scripts/` | Already split (`ci`, `coverage`, `ratchets`, …) | Healthier; keep meta here |

### 1.2 Locked product facts (do not contradict)

From `docs/product-architecture.md` + E-MOD0:

- **One installable CLI** (`doc-engine`) hosting several DDD BCs — not microservices.
- Layers today: **Kernel** (`src/doc_engine`), **Pipeline tools** (`doc_engine.tools`), **Adapters** (`adapters/`).
- **Product vs meta:** wheel ≠ `scripts/` self-check policy.
- Embody: hexagonal ports, vertical/concept slices, tach cycle gate; Refuse: `utils/`, DI containers, mesh/Backstage.

### 1.3 Category errors to refuse up front

| Error | Why |
| --- | --- |
| “Make folders deeper” without fitness | Boundaries erode; E-TACH0 |
| Big-bang `tests/<bc>/` move as v1 | Claim/path churn; E-TEST0 **Refuse** first move |
| Layer-first `domain/` / `application/` at repo top | Wrong axis for multi-BC CLI; E-MOD M4 vertical |
| Copy Nx `apps/`/`libs/` or Packwerk Ruby packs as deps | Wrong runtime; pattern-only |
| Dual writers during migrate (old + new import paths forever) | DDIA SoR vs derived; strangler needs exit |

---

## 2. Evidence inventory

### 2.1 In-repo SoR `[Confirmed]`

| Source | Signal |
| --- | --- |
| E-MOD0 / M1–M5 | Several BCs in one CLI; vertical under packages; Protocol ports; no utils/DI |
| E-TEST0 | Markers + CI shards **before** physical test moves |
| E-TACH0 | Dependency map as blueprint; layers → `depends_on` + interfaces; no sync-as-Spec |
| DDIA north star domain 05 | Maintainability / evolvability — structure serves change, not ceremony |
| `tach.toml` today | Only `doc_engine` + `stf` modules; cycles forbidden; **no** `depends_on` / layers yet |

### 2.2 External primary `[Evidenced]`

| Source | Use |
| --- | --- |
| [tach docs — configuration / layers / `tach.domain.toml`](https://docs.gauge.sh/usage/configuration/) | Python BC packs + public interfaces + incremental monorepo `source_roots` |
| [Shopify Packwerk](https://shopify.engineering/enforcing-modularity-rails-apps-packwerk) | Package privacy + declared deps — **pattern only** |
| [arXiv:2401.11867](https://arxiv.org/abs/2401.11867) Modular monolith survey | Modules as units with exposed API; Spring Modulith / Service Weaver as *pattern* references |
| DDD 2026 practice (strategic BCs > tactical `domain/` folders) | Folder named `domain/` ≠ bounded context |
| Nx enforce-module-boundaries / Go nested `internal/` | Language-specific enforcement — steal *idea*, not toolchain |

### 2.3 Open `[Unknown]` until spike

- Exact import graph cost of Option C (multi-`pyproject`) on editable install + CI wall-clock.
- Whether `tools/` natural BCs are ≥4 stable clusters or still one “deterministic toolkit” context with subfolders.
- CODEOWNERS / agent-path claim rewrites volume for Option B root move.

---

## 3. Six repository structure options

Each option includes: intent, sketch tree, fits this product?, Embody/Adopt/Refuse/Defer, migration risk.

### Option A — Vertical bounded contexts inside one wheel (deepen in place)

**Intent.** Keep `src/doc_engine` + `src/stf` as the installable surface. Replace fat packages with **concept BCs** and thin façades. Mirror tests gradually under `tests/doc_engine/<bc>/` *after* markers.

```
src/
  doc_engine/
    cli/                 # presentation / composition root
    core/                # shared kernel (minimal)
    pipeline/            # BC: orchestration + artifacts ACL
    scanning/            # BC: Stage-0 signals / backends
    query/               # BC: query surface
    compliance/          # BC: profiles + certification (today partly under tools/ci)
    ci_sensors/          # BC: coverage measure / climb (today doc_engine.ci)
    tools/               # shrink → invoke façades only, or dissolve into BCs
  stf/                   # BC: semantic test framework (already separate)
tests/
  doc_engine/
    pipeline/
    scanning/
    …
adapters/                # unchanged role
scripts/                 # meta unchanged
```

| Stance | **Embody** as primary *code* layout (aligns E-MOD M1/M4, TACH3) |
| Migration | Medium — incremental `git mv` + façade re-exports; import paths change inside package |
| Enforcement | tach layers + `depends_on` + `[[interfaces]]` (E-TACH1–2) |

**Pros:** Matches locked product model; lowest packaging churn; works with current setuptools find.  
**Cons:** Root shallowness remains; `tools/` dissolution needs careful strangler.

---

### Option B — Root tripartition: product / meta / policy

**Intent.** Fix *root* shallow mix by grouping deployable product, repo-ops meta, and agent/policy packs — still one git repo.

```
product/
  src/doc_engine/ …
  src/stf/
  adapters/
  spring-signals/
  skills/                 # or only adapters/*/skills
  pyproject.toml          # or keep root pyproject with package-dir map
meta/
  scripts/
  tests/                  # or tests stay root for pytest convention
  codeql/
  .github/
policy/                   # agent hooks / CLAUDE / .cursor bridges
  adapters/claude/hooks/  # OR keep adapters; put only .claude/.cursor here
docs/                     # stays top-level (already domain-mapped)
```

| Stance | **Adopt selectively** for *documentation of boundaries*; physical root move **Defer** until claims/hooks inventory spike |
| Migration | High — almost every path claim, hook, CI, plugin manifest |
| Enforcement | Conventions + README maps; tach still on `src` |

**Pros:** Makes product vs meta (already in product-architecture) visible at root.  
**Cons:** Massive path churn for little runtime gain; Cloud/Claude hook paths brittle.

**Variant B′ (low churn):** keep physical paths; add a **root DOMAIN_MAP.md** + CODEOWNERS zones — Adopt now as documentation SoR without `git mv`.

---

### Option C — Multi-package workspace monorepo (apps + libs)

**Intent.** Nx/uv-workspace style: each BC is its own Python distribution; CLI is a thin app composing libs.

```
packages/
  doc-engine-core/
  doc-engine-pipeline/
  doc-engine-scanning/
  doc-engine-query/
  doc-engine-compliance/
  stf/
apps/
  doc-engine-cli/         # depends on packages via path deps
pyproject.toml            # uv/poetry workspace root
tach.toml                 # source_roots = each package/src
```

| Stance | **Defer** (possibly refuse for years) — product is one CLI/wheel for customers |
| Migration | Very high — publish/install story, import renames, CI matrix |
| Enforcement | `tach check-external` + per-package deps `[Evidenced]` tach monorepo docs |

**Pros:** Hard packaging boundaries; independent versioning *if* ever needed.  
**Cons:** Overkill for one `pip install doc-engine`; fights “portable single wheel”; dual SoT risk across `pyproject`s.

---

### Option D — Colocated vertical slices (code + tests + fixtures per domain)

**Intent.** Maximize cohesion: everything for a BC lives together.

```
domains/
  scanning/
    src/doc_engine_scanning/
    tests/
    fixtures/
    schemas/
    tach.domain.toml
  pipeline/
    …
  stf/
    …
meta/scripts/
adapters/
```

| Stance | **Refuse** as big-bang; **Adopt ideas** only (keep fixtures near scanners *inside* existing trees) |
| Migration | Extreme — pytest roots, coverage paths, claims, egg layout |
| Enforcement | Per-domain tach.domain.toml `[Evidenced]` |

**Pros:** Ideal navigability for large multi-team products.  
**Cons:** Breaks this repo’s established `src/` + `tests/` + `scripts/fixtures` SoR; PathCohesion / claims blast radius.

---

### Option E — Layer-first Clean Architecture packages

**Intent.** Classic rings at the top of `src/`.

```
src/
  domain/           # entities / value objects across all BCs
  application/      # use cases
  infrastructure/   # scanners, fs, subprocess
  presentation/     # CLI
```

| Stance | **Refuse** as primary taxonomy |
| Migration | High rewrite; collapses multiple ubiquitous languages into one “domain” bag |
| Enforcement | Layer rules only — weak BC isolation |

**Pros:** Familiar to Clean Architecture tutorials.  
**Cons:** Strategic DDD says **BC first**, layers *inside* BC; recreates shared-kernel bloat; contradicts E-MOD M4.

---

### Option F — Packwerk-style packs + public surfaces (tach-native)

**Intent.** Keep Option A’s BC folders, but make **privacy + deps** the structuring mechanism: each BC exposes only a public façade; optional colocated `tach.domain.toml`.

```
src/doc_engine/
  scanning/
    __init__.py          # public façade only
    public/              # or services/ listed in [[interfaces]] expose
    internal/            # backends, astgrep, gap_probe (not importable cross-BC)
    tach.domain.toml     # optional ownership split
  pipeline/
    __init__.py
    public/
    internal/
    …
  tools/                 # shrink to registry of entrypoints → BC public APIs
```

| Stance | **Adopt** as enforcement layer **on top of Option A** (E-TACH Embody/Adopt) |
| Migration | Medium — mostly import discipline + façades; physical `internal/` optional |
| Enforcement | tach `[[interfaces]]` + `depends_on`; Packwerk pattern without Ruby `[Evidenced]` |

**Pros:** Folder structure *means* something in CI; matches “dependencies as blueprint.”  
**Cons:** Requires cycle break first (TACH4); `internal/` naming is convention unless tach interfaces back it.

---

## 4. Comparison matrix

| Criterion | A Vertical BC | B Root zones | C Workspace pkgs | D Colocated | E Layer-first | F Pack+tach |
| --- | --- | --- | --- | --- | --- | --- |
| Matches one-wheel CLI | ✓ | ~ | ✗ | ~ | ~ | ✓ |
| Fixes fat `tools/` / tests | ✓ | ✗ | ✓ | ✓ | ✗ | ✓ |
| Fixes shallow root | ✗ | ✓ | ~ | ✓ | ✗ | ✗ |
| Churn / claims blast | Med | High | Very high | Extreme | High | Med |
| Aligns E-MOD/E-TACH/E-TEST | ✓ | Partial | Weak | Conflicts E-TEST v1 | Conflicts M4 | ✓ |
| Enforcement story | tach | Docs/CODEOWNERS | tach-external | tach.domain | layers only | tach interfaces |
| Recommended stance | **Embody** | **Defer physical / Adopt map** | **Defer** | **Refuse bang** | **Refuse** | **Adopt** |

---

## 5. Embody / Adopt / Refuse / Defer (REPO1–REPO8)

| ID | Decision | Stance |
| --- | --- | --- |
| **REPO1** | Primary code taxonomy = **bounded contexts** (pipeline, scanning, query, compliance/cert, ci-sensors, stf, adapters, meta-scripts) — not technical layers at repo top | **Embody** |
| **REPO2** | Prefer **Option A + F**: deepen BC packages + tach public interfaces; dissolve `tools/` grab-bag into BC façades over strangler | **Adopt** |
| **REPO3** | Physical **Option B** root move requires a dedicated claims/hooks spike; until then use DOMAIN_MAP / CODEOWNERS (B′) | **Defer** physical · **Adopt** B′ |
| **REPO4** | Multi-package workspace (**Option C**) only if a future product decision splits publishable artifacts | **Defer** |
| **REPO5** | Colocated domains (**Option D**) big-bang | **Refuse** |
| **REPO6** | Layer-first top packages (**Option E**) | **Refuse** |
| **REPO7** | Test topology: **markers + CI shards first**; directory moves follow E-TEST0 — never invert | **Embody** |
| **REPO8** | No structure PR may weaken fail_under 98.7 / complexipy≤5 / LOC≤225 / PathCohesion / introduce utils/ | **Embody** |

---

## 6. Target context map (draft ubiquitous language)

```text
[Meta CI / claims] ----(ACL)----> reads product packages for quality gates only
[Adapters: Claude|Cursor|GH] ----> call [CLI façade] only
[CLI façade] ----> [Pipeline BC] ----> ports ----> [Scanning BC]
                 |-> [Query BC]
                 |-> [Compliance BC]
[CI-sensors BC]  (coverage oracle/climb) — product-adjacent, not customer Stage-0
[STF BC]         — parallel package; tach sibling of doc_engine
[Spring-signals pack / fixtures] — Stage-0 corpus SoR (not wheel guts)
```

Shared kernel (`doc_engine.core`, paths, config) stays **minimal**. Cross-BC types cross via ACL DTOs (`pipeline/artifacts`, validators) — already named in product-architecture.

---

## 7. Adversarial checklist

- [ ] Does Approve authorize renaming root folders tomorrow? — **No** without REPO3 spike exit.
- [ ] Can agents treat this memo as license to `git mv tests/`? — **No** (REPO7 / E-TEST0).
- [ ] Is Option F “add `internal/` folders” enough without tach interfaces? — **No** (folder cosplay).
- [ ] Does dissolving `tools/` recreate a `utils/`? — **Refuse**; each move needs a concept name.
- [ ] Will workspace packages help marketplace plugin packing? — Unproven; adapters already separated.
- [ ] Does deeper nesting fight docs/research “≤2 levels” rule? — That rule is for **research docs**, not `src/` BCs.

---

## 8. Epic sketch (fresh-chat ready)

### E-REPO0 — Spec gate (this memo)
- **Goal:** Approve REPO1–REPO8 (or record deltas).
- **Exit:** `spec_gate: APPROVED E-REPO0` + backlog pointer.
- **Non-goal:** mass moves.

### E-REPO1 — Map + façades (Implement, after E-COH / cycle work)
| ID | Title | Acceptance |
| --- | --- | --- |
| REPO1-1 | Publish root `DOMAIN_MAP.md` (B′) listing BCs ↔ paths | claims path resolves; linked from README |
| REPO1-2 | Inventory `tools/*.py` → target BC table | every file tagged; no orphan |
| REPO1-3 | Strangler: first BC façade + tach interface for one fat edge | `tach check` green; no deep import |
| REPO1-4 | Align test markers to same BC names (E-TEST1) | markers documented; unlabeled → serial |

### Spikes
| ID | Question | Exit |
| --- | --- | --- |
| REPO-S1 | Physical Option B path-churn cost (hooks, action.yml, plugin manifests) | go/no-go memo |
| REPO-S2 | Natural clusters inside `tools/` (ast-grep / import graph) | BC cut list or “keep toolkit + subpackages” |

**Invariants:** constitution gates; one tip writer; Spec → Implement → Verify → Archive.

---

## 9. Ranking for *this* tip (human Approve)

**Approve packet = memos 21 + 22 + 23 (REPO1–REPO20).**

Capability-aware composition (memo 23 §4):

1. **Wave 0:** Possibility 1 overlay + logical truth labels + scream names in the map.  
2. **Wave 1:** Possibility 2 deep BC+tach spine + Possibility 3 stage dialect to dissolve `tools/`.  
3. **Wave 1b:** Possibility 5 multi-base *pattern* sketch; Possibility 7 agent-pack maps.  
4. **Wave 2:** Possibility 6 Hive only in hot scanner/pipeline BCs; physical truth zones if overlay fails.  
5. **Wave 3:** Possibility 8 / physical bases only after H3 multi-repo or HttpLLM product Spec.

Keep refuse set (memo 23 Possibility 10). Sequence with **E-COH / E-TACH / E-TEST** — no mass moves during H1 Stage-4 calibration.

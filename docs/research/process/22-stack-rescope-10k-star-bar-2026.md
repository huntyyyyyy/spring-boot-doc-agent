---
title: E-STACK0 — Stack rescope under ≥10k★ SoR bar (2026)
status: DRAFT Spec — pending Approve of STACK1–STACK12
research date: 2026-08-09
research_window: 2026-06-01 → 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`)
related:
  - docs/research/process/21-post-merge-gate-repair-cohesion-2026.md
  - docs/research/process/04-implementation-frameworks.md
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
  - requirements.txt
  - requirements-dev.txt
  - tach.toml
do_not:
  - swap tools mid-hotfix without Spec (E-HOT still first for red main)
  - adopt Spec Kit WorkflowEngine as runtime because it clears ★ (constitution Refuse)
  - dual-wire SonarQube as fail_under / complexipy replacement without Spec
  - raise LOC/complexipy/fail_under ceilings
  - cite &lt;10000★ GH as *new* implement SoR
spec_gate: DRAFT E-STACK0 (2026-08-09) — STACK1–STACK12 pending Approve
gh_sor_bar: "≥10000★ and pushed_at within research_window; Confirmed in-repo pins may Embody-continue"
---

# Principal memo: rescope stack choices under ≥10k★

**Question.** Given the raised GitHub implement SoR bar (**≥10,000★** + recent push),
which frameworks and tools this repo has already Embodied/Adopted still clear the
bar, where higher-adoption peers **improve** or **worsen** the product if substituted,
and what should change in Spec / Implement order?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

**Star snapshot:** GitHub API **2026-08-09** (this session). Stars alone never Adopt.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Must we rip out every &lt;10k★ pin tomorrow? | **No.** HOT13 / STACK exemption: **Confirmed** CI pins may **Embody-continue**. New *Adopts* and *expansions* must clear ≥10k★ **or** be Explicit Confirmed+Approve without ★ pretence. |
| What already clears ≥10k★? | **ruff** (~49k), **pytest** (~14k), **ast-grep** (~15k), **semgrep** (~16k), **mypy/pyright** (type peers ~20k/~15k), **black** (~42k, subsumed by ruff), **Nx** (~29k patterns), **Spec Kit** (~126k process), **mkdocs-material** (~27k), **SonarQube** (~11k). |
| What fails ★ but is pinned today? | **tach** (~2.8k), **complexipy** (niche; search Unconfirmed ★), **coverage.py** (~3.4k), **pytest-cov** (~2.0k), **CodeQL** (~9.9k — under by ~77), **PyYAML** (~2.9k), **mutmut/Hypothesis** (not pinned; prior Spike). |
| Biggest *concept* steal from ≥10k★? | **Nx module-boundary + public API discipline** (patterns) → drive E-TACH0/E-COH seam maps; **pytest** patch-at-use; **Spec Kit / OpenSpec SDD** process (already Adopt) — **not** Spec Kit runtime. |
| Biggest *substitution risk* (worsens)? | Replacing ruff with flake8+black; replacing tach cycles with pylint plugins (&lt;10k); making SonarQube the **boolean** complexipy/fail_under SoT; installing Spec Kit WorkflowEngine; DI/mesh theater. |
| Order vs red `main`? | **E-HOT0/1 first** (gates green). **E-STACK0 Approve** can land in parallel as *docs Spec*. Tool swaps only after green + Approve. |

---

## 1. Confirmed stack inventory (what we actually run)

### 1.1 Runtime (`requirements.txt`) `[Confirmed]`

| Pin | Role |
| --- | --- |
| `ast-grep-cli~=0.45` | Structural search / Stage-0 scanner backend |
| `semgrep~=1.171` | Rule pack / FP baseline twin |
| `sqllineage`, `pathspec` | Pipeline helpers |

### 1.2 Dev / gates (`requirements-dev.txt`) `[Confirmed]`

| Pin | Role |
| --- | --- |
| `ruff~=0.16` | Lint+format (C901 off; complexipy owns cognitive) |
| `pytest~=8.3`, `pytest-cov~=6` | Tests + coverage adapter |
| `complexipy~=6.2` | Cognitive ≤5 hard gate |
| `tach~=0.35` | Import **cycle** gate only (`tach.toml`: free deps, `forbid_circular_dependencies`) |
| `diff-cover`, `PyYAML`, `mkdocs-material` | New-code cover / workflow YAML / docs site |

### 1.3 External binaries / SaaS `[Confirmed]`

| Tool | Role | Policy |
| --- | --- | --- |
| CodeQL CLI | Signals pack / Stage-0 corpus | Required BC jobs |
| SonarCloud | Non-blocking workflow | Explicitly **not** policy SoT |
| jscpd (npm) | Copy-paste gate | quality-gates |

### 1.4 Concept frameworks already Embodied/Adopted (not pip pins)

| Framework | Stance (synthesis / E-MOD* / E-COH*) | ★ nature |
| --- | --- | --- |
| DDD BCs + vertical slices | Embody | Classic / process |
| Hexagonal ports / Protocol strategies | Adopt | Classic |
| OpenSpec-style SDD deltas | Adopt | Process (Spec Kit clears ★; runtime Refuse) |
| Oracle vs climb dual-mode | Embody | pytest-cov mechanics |
| Façade poke + research hooks | Embody | pytest culture |
| E-TACH0 depends_on + interfaces | Draft | tach &lt;10k★ |

---

## 2. ★ scoreboard (Evidenced 2026-08-09)

| Tool / peer | ★ | ≥10k? | Our use |
| ---: | ---: | --- | --- |
| github/spec-kit | 125982 | Yes | Process peer only |
| astral-sh/ruff | 49115 | Yes | **Pinned** lint/format |
| psf/black | 41787 | Yes | Subsumed by ruff |
| nrwl/nx | 29207 | Yes | **Pattern** for boundaries |
| squidfunk/mkdocs-material | 27232 | Yes | **Pinned** docs |
| python/mypy | 20587 | Yes | Not pinned (annotation ratchet instead) |
| vitest / jest (JS) | 16k–45k | Yes | Pattern only (test intentionality) |
| semgrep/semgrep | 16162 | Yes | **Pinned** |
| microsoft/pyright | 15578 | Yes | Not pinned |
| ast-grep/ast-grep | 15455 | Yes | **Pinned** |
| pytest-dev/pytest | 14397 | Yes | **Pinned** |
| SonarSource/sonarqube | 10882 | Yes | SaaS advisory only today |
| github/codeql | 9923 | **No** | **Pinned** binary |
| HypothesisWorks/hypothesis | 8856 | **No** | Spike / missing pin |
| pylint-dev/pylint | 5710 | **No** | Not used |
| PyCQA/flake8 | 3810 | **No** | Replaced by ruff |
| TNG/ArchUnit | 3794 | **No** | Java pattern peer |
| nedbat/coveragepy | 3404 | **No** | Transitive via pytest-cov |
| yaml/pyyaml | 2929 | **No** | **Pinned** |
| tach-org/tach | 2786 | **No** | **Pinned** cycles |
| pytest-dev/pytest-cov | 2054 | **No** | **Pinned** |
| boxed/mutmut | 1379 | **No** | Not pinned |
| spring-projects/spring-modulith | 1162 | **No** | Pattern only |

`complexipy`: niche package; treat as **&lt;10k / Confirmed pin** until a ≥10k★ cognitive gate is Spec’d.

---

## 3. Layer-by-layer: keep / steal / refuse (improve vs worsen)

Legend: **Improve** = clearer fitness, less thrash, better ecosystem SoR · **Worsen** = noise, wrong product shape, dual SoT, or ★ theater.

### 3.1 Lint & format

| Choice | Stance under 10k★ | vs higher-adoption |
| --- | --- | --- |
| **Keep ruff** | Embody (clears ★) | vs flake8+black+isort: **Improve** (one tool, already chosen). vs pylint: **Improve** (speed; pylint fails ★). |
| Reintroduce flake8/black | Refuse | **Worsens** tip thrash and CI time |

### 3.2 Tests & intentionality

| Choice | Stance | vs higher-adoption |
| --- | --- | --- |
| **Keep pytest** | Embody (clears ★) | Industry default; monkeypatch doctrine SoR for E-HOT F2 |
| Jest/Vitest concepts | Adopt *patterns* only | **Improve** intentionality culture; **Worsen** if runtime swap |
| Hypothesis | Defer (fails ★; not pinned) | Property tests useful for pure helpers (E-QA3) but not ★-justified merge SoR |
| mutmut | Defer/Refuse as merge SoR | Fails ★; adequacy sensor only (E-QA) |

### 3.3 Coverage oracle

| Choice | Stance | vs higher-adoption |
| --- | --- | --- |
| **coverage.py + pytest-cov** | Embody-continue (**Confirmed**; both fail ★) | No ≥10k★ Python coverage engine exists. **Worsens** if we invent a second oracle. |
| Sonar coverage as floor | Refuse | **Worsens** — dual SoT with `coverage.xml` / fail_under 98.7 |
| Keep policy 16-A climb XML | Embody | Independent of ★ |

### 3.4 Structural search / Stage-0

| Choice | Stance | vs higher-adoption |
| --- | --- | --- |
| **Keep ast-grep + semgrep** | Embody (both clear ★) | Complementary: structural citations vs rule packs. Dropping either **worsens** Stage-0 SoR |
| CodeQL | Embody-continue (Confirmed; ★ 9923) | Just under bar — **do not** expand as *new* Adopt via ★; keep existing jobs. SonarQube (≥10k) is **not** a CodeQL substitute for pack/corpus gates |

### 3.5 Architecture fitness (the sharp edge)

| Choice | Stance | Improve / worsen |
| --- | --- | --- |
| **tach cycles only** (today) | Embody-continue Confirmed; **not** ★ SoR | Correct minimal fitness. Expanding `depends_on` *because research 20 liked tach* **worsens** under HOT13 (★ fail) |
| **Nx enforce-module-boundaries** concepts | Adopt *patterns* (≥10k★) | **Improves** seam-map vocabulary for E-COH / E-TACH Spec: tags, public API, acyclic graph |
| ArchUnit / Spring Modulith | Pattern only (fail ★) | Concepts OK; Java runtime **worsens** |
| import-linter / PyTestArch / pylint-boundaries | Refuse dual-gate / fail ★ | Dual fitness **worsens** (FAC4 / LEG-S1) |
| In-repo thin depends_on checker | Spike after E-HOT green | **May improve** if tach ★ remains low and E-TACH0 wants interfaces without pretending tach clears SoR — still Prefer tach *implementation* if Approve names Confirmed pin explicitly |
| mypy/pyright as architecture SoT | Refuse | Types ≠ BC edges; **worsens** if they replace tach/claims |

**Rescope for E-TACH0:** rewrite Spec so primary *external* SoR is **Nx-class boundary patterns (≥10k★)** + arXiv governance; tach is **Confirmed implementation vehicle** (or Spike replace), not the ★ justification.

### 3.6 Cognitive / size gates

| Choice | Stance | Improve / worsen |
| --- | --- | --- |
| **complexipy ≤5** | Embody-continue Confirmed | Niche ★ — keep until Spec names Sonar cognitive as *sensor* only |
| SonarQube cognitive (≥10k★) | Adopt as **advisory** parallel only | **Improves** external SoR narrative; **worsens** if promoted to boolean merge SoT (already Refuse Sonar as policy) |
| ruff C901 | Refuse as replacement | McCabe ≠ complexipy; synthesis already Refuse McCabe sole SoT |
| LOC≤225 / stmts≤20 in-repo | Embody | No GH★ tool owns this; cohesion bar (E-COH) is the design SoR |

### 3.7 Process / SDD / agent frameworks

| Choice | Stance | Improve / worsen |
| --- | --- | --- |
| OpenSpec-style deltas + living memos | Embody/Adopt | Fits brownfield CLI |
| Spec Kit (≥126k★) | Adopt *process lessons* only | **Improves** Spec ceremony vocabulary; **Worsens hard** if WorkflowEngine becomes runtime (constitution Refuse) |
| Backstage / mesh / DI containers | Refuse | ★ irrelevant — wrong product |

### 3.8 Docs publishing

| Choice | Stance |
| --- | --- |
| mkdocs-material | Embody (clears ★) — keep |

---

## 4. Net rescope (what changes vs what does not)

### 4.1 Do **not** change in E-HOT1 (hotfix)

Pins and gate semantics stay. Hotfix restores contracts under current tools.

### 4.2 Spec changes on Approve (STACK*)

| ID | Decision |
| --- | --- |
| **STACK1** | Repo stream SoR for *new* tools/framework Adopts: **≥10k★** + push in window (align HOT13) |
| **STACK2** | Confirmed pins may Embody-continue without ★; expansions of those tools need Explicit Approve naming the pin |
| **STACK3** | Keep ruff, pytest, ast-grep, semgrep, mkdocs-material (clear ★) |
| **STACK4** | Keep coverage.py/pytest-cov as coverage oracle adapters despite ★ (no ≥10k peer); refuse Sonar as floor |
| **STACK5** | Keep CodeQL jobs as Confirmed; do not cite ★ for new CodeQL surface area until ≥10k or re-Approve |
| **STACK6** | tach: **cycle gate only** until E-TACH0 re-Spec under Nx-pattern SoR; no `depends_on`/`[[interfaces]]` expansion justified by tach ★ |
| **STACK7** | complexipy: keep ≤5 Confirmed; Sonar cognitive may be advisory sensor only — never replace boolean complexipy without new Spec |
| **STACK8** | Steal **Nx boundary + public API** concepts into E-COH1 / E-TACH0 seam maps (patterns, not Nx install) |
| **STACK9** | Spec Kit / OpenSpec: process Adopt only; WorkflowEngine runtime remains Refuse |
| **STACK10** | Refuse dual architecture linters; refuse flake8/black reintroduction; refuse DI/mesh/Backstage |
| **STACK11** | Hypothesis/mutmut remain Spike/Defer — fail ★ for new merge SoR |
| **STACK12** | Implement order: **E-HOT1 green → E-STACK0 Approve (docs) → resume E-COH1**; tool rip/replace only under a later epic after green |

### 4.3 Where higher-adoption **improves** us (actionable)

1. **Patch-at-use** (pytest ≥10k) — E-HOT F2.
2. **Nx-shaped seam maps** before file moves — E-COH1 / E-TACH0.
3. **SDD ceremony** from Spec Kit popularity without importing its engine.
4. **Single-toolchain lint** (ruff) validated by ★ vs fragmented flake8 era.

### 4.4 Where chasing ≥10k★ **would worsen** us

1. Spec Kit / Sonar / Nx as **runtime or boolean SoT**.
2. Dropping tach cycles with no replacement (cycle refuse is load-bearing).
3. Dropping complexipy for Sonar QG (non-blocking today by design).
4. Adding mypy/pyright *and* treating them as architecture gates (noise + dual SoT).
5. Replacing ast-grep with “just semgrep” or vice versa (different predicates).

---

## 5. Adversarial checklist

- [ ] Does ≥10k★ force deleting tach tomorrow? — **No (STACK2/6).**
- [ ] Does Spec Kit ★ overturn WorkflowEngine Refuse? — **No (STACK9).**
- [ ] Is SonarQube ≥10k a license to own fail_under? — **No (STACK4/7).**
- [ ] Can E-TACH0 still cite tach ★ as primary SoR? — **No; re-base on Nx patterns + Confirmed pin (STACK6/8).**
- [ ] Does stack rescope delay fixing red main? — **Must not; E-HOT1 first (STACK12).**
- [ ] Are classic DDD/hexagonal “invalid” without GitHub ★? — **No; not GH tools.**

---

## 6. Epic sketch

### E-STACK0 — Spec gate (this memo)

Exit: Approve STACK1–STACK12; backlog P19.0; cross-link E-HOT0 HOT13; note E-TACH0 draft must amend ★ justification.

### E-STACK1 — Optional later (after E-HOT1 + E-COH1 progress)

Only if Approve asks: document Confirmed-pin register; amend E-TACH0 research ★ section; optional Spike “in-repo depends_on” vs tach expansion.

**Invariants:** constitution gates; one tip writer; no utils/; local full-gate before push.

---

## 7. Embody / Adopt / Refuse / Defer

| Stance | Item |
| --- | --- |
| **Embody** | ruff, pytest, ast-grep, semgrep, mkdocs-material; DDD/ports/vertical slices; oracle/climb policy; tach **cycles**; complexipy ≤5; coverage.xml floor |
| **Adopt** | ≥10k★ bar for *new* SoR; Nx boundary **patterns**; pytest patch-at-use; OpenSpec/Spec Kit **process** lessons; STACK order after HOT |
| **Defer** | tach depends_on/interfaces; Hypothesis/mutmut merge; mypy/pyright as required gates; global rewrite of older ≥1k★ memos |
| **Refuse** | Spec Kit runtime; Sonar/Cover% as fail_under; flake8+black return; dual arch linters; DI/mesh/Backstage; ★-washing &lt;10k tools as *new* Adopt |

---

## 8. Exit

**E-STACK0 DRAFT** until human Approve of STACK1–STACK12.
Does **not** authorize product tool swaps. Complements E-HOT0 (gates) and re-bases
E-TACH0/E-COH1 framework language on ≥10k★ peers where ★ was doing load-bearing work.

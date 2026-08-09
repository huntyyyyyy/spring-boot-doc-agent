---
segment: 01
title: Coverage oracle vs climb — DDIA SoT, SOLID/DRY/OCP, complexipy, naming
status: RESEARCH COMPLETE — informs design approval; dual-mode NOT implemented
research date: 2026-08-08
branch: wave1-gates-untrusted-tree-hygiene
claim tiers: Evidenced / Confirmed / Unknown
related:
  - docs/design/coverage-measure-modes-design-2026-08-08.md
  - docs/design/ddia-north-star/domains/01-data-flow-and-truth/concepts/system-of-record-vs-derived.md
  - docs/design/ddia-north-star/playbooks/choosing-sor-vs-view.md
  - docs/agentic-foundational-se-taxonomy-2026-08-08.md
do_not:
  - implement dual-mode in this pass
  - touch sibling research paths
---

# Segment 01: Coverage oracle vs climb (SOLID / DDIA / gates)

> Dual-mode remains **design-only**. This segment amends decisions for
> SoT hygiene, SOLID/OCP shape, cognitive complexity, naming, and the
> pytest-cov trap: **scoped `--cov` Cover% ≠ whole-repo `fail_under`**.

**Claim tiers:** `[Evidenced]` = primary paper/docs/issues cited ·
`[Confirmed]` = this checkout’s seams + CONTRIBUTING agree ·
`[Unknown]` = needs product choice or measurement.

---

## 1. Problem (one artifact, two jobs)

Today `MeasureRun` is a single unlabeled path: wipe → full
`pytest tests/ --cov=doc_engine --cov=stf --cov-branch` →
`--cov-fail-under=<floor>` → cohesive `coverage.xml`.
`[Confirmed]` `src/doc_engine/ci/coverage_measure.py`.

That path is treated as:

| Role | Needed granularity | Cost |
| --- | --- | --- |
| **Oracle / SoT** | Whole-repo Cover% vs 98.7 | Full suite; CI 3.11 only |
| **Climb sensor** | Package/file missing lines | Should be cheap & scoped |

Collapsing them forces agents to pay oracle wall-clock for every climb
batch, and invites the worse failure: a **scoped** pytest-cov total that
still carries `--cov-fail-under=98.7` being mistaken for repo floor proof.

CONTRIBUTING already separates whole-repo `fail_under`, new-code
`diff-cover`, and below-floor gap-average inventory.
`[Confirmed]` CONTRIBUTING coverage table (~fail_under 98.7 /
gap-average / PathCohesion). The CLI does not yet expose a labeled climb
mode. `[Confirmed]` design memo status AWAITING CONFIRMATION.

---

## 2. External sources (verified this pass)

### 2.1 arXiv — CoverUp `[Evidenced]`

[CoverUp: Coverage-Guided LLM-Based Test Generation](https://arxiv.org/abs/2403.16218)
(arXiv:2403.16218; also [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2403.16218)).

- Iterates: measure coverage → segment by **missing** lines/branches →
  prompt/refine → remeasure.
- Iterative coverage guidance ≈ half of successes (paper claim).
- Final acceptance still implies a **whole-suite** coverage check, not a
  permanent substitute of segment metrics for global coverage.

**Repo map:** climb ≈ CoverUp’s inner measure-on-segments loop; oracle ≈
final whole-suite acceptance. Do not skip the final oracle.

### 2.2 arXiv — ChaCo `[Evidenced]`

[Change And Cover (ChaCo)](https://arxiv.org/abs/2601.10942)
(arXiv:2601.10942) — PR/patch-scoped last-mile augmentation.

- Optimizes **patch coverage** for a PR, not whole-repo floor climb.
- Orthogonal to below-floor gap-average inventory (unchanged green files
  stay out of gap-average by design). `[Confirmed]` CONTRIBUTING.

**Repo map:** ChaCo ≈ kin of `diff-cover` / new-code gate, **not** the
climb targeting SoT for files already below 98.7.

### 2.3 pytest-cov primary docs `[Evidenced]`

[pytest-cov configuration](https://pytest-cov.readthedocs.io/en/latest/config.html):

- `--cov=PATH` **overrides** coverage’s `[run] source`.
- `--cov-fail-under=MIN` fails if **total coverage of the measured
  sources** is less than MIN — not “repo truth if you narrowed source.”

Implication: `pytest --cov=doc_engine.ci --cov-fail-under=98.7` is a
**different predicate** than whole-repo 98.7 over `doc_engine`+`stf`.
Using the same flag unlabeled creates a hidden SoT.

### 2.4 GitHub — pytest-cov subset reporting `[Evidenced]`

[pytest-cov#528](https://github.com/pytest-dev/pytest-cov/issues/528)
(closed): subset `--cov` reporting / XML packaging differs from raw
`coverage run --source=…` then `coverage xml`. Confirms that narrowing
source changes what “total” means and how artifacts look — another reason
climb must not silently overwrite the oracle XML contract.

### 2.5 DeepWiki — pytest-cov controllers (secondary) `[Evidenced]`

[Coverage Controllers and Execution Modes](https://deepwiki.com/pytest-dev/pytest-cov/2.2-coverage-controllers-and-execution-modes)
(DeepWiki over `pytest_cov.engine`): `Central` / `DistMaster` /
`DistWorker`; suffix’d data files; master combine on xdist.

- Fine **inside one checkout**.
- Dangerous if agents treat worker shards as oracle or combine across
  worktrees — already forbidden here by PathCohesionGuard / single-writer.
  `[Confirmed]`

Treat DeepWiki as **secondary cartography** of primary source; prefer
pytest-cov docs + engine.py if implementing xdist later.

### 2.6 coverage.py path / combine hazards `[Evidenced]`

Primary docs + issues already cited in the design memo
([cmd_combine](https://coverage.readthedocs.io/en/latest/commands/cmd_combine.html);
[#903](https://github.com/nedbat/coveragepy/issues/903),
[#991](https://github.com/nedbat/coveragepy/issues/991),
[#1752](https://github.com/coveragepy/coveragepy/issues/1752),
[#2072](https://github.com/coveragepy/coveragepy/issues/2072)).
This tree’s answer is already landed: wipe local artifacts; never combine
across `wt-*` trees. `[Confirmed]`

---

## 3. DDIA SoT mapping (this repo)

From local DDIA north-star:
[`system-of-record-vs-derived`](../design/ddia-north-star/domains/01-data-flow-and-truth/concepts/system-of-record-vs-derived.md)
and [`choosing-sor-vs-view`](../design/ddia-north-star/playbooks/choosing-sor-vs-view.md).
`[Confirmed]`

| Artifact | Role | Wins on disagreement? |
| --- | --- | --- |
| Fresh cohesive full `coverage.xml` from `mode=oracle` (3.11 / MeasureRun) | **SoR** for whole-repo Cover% | Yes — only path that may assert 98.7 |
| `coverage-gap-average` below-floor list | **Derived** targeting view | Rebuild from last cohesive oracle XML |
| Scoped climb Cover% / missing lines | **Derived** accelerator sensor | Never substitutes for fail_under |
| `diff-cover` vs merge-base | **Hard gate** for *new code* only | Independent of climb inventory |
| Stale XML from another worktree | Invalid | PathCohesionGuard exit 2 |

**Dual-write anti-pattern:** climb writing the same `coverage.xml` path
oracle readers treat as SoR without a distinct name or refuse-write
policy. Product choice still open (`[Unknown]` until decision 16 recorded).

**Operability:** predictable modes, good defaults, visible banners —
agents must see `mode=climb (not CI oracle)` on stderr.

---

## 4. SOLID / DRY / OCP against decisions 1–12

| Principle | Score of 1–12 alone | Gap | Fix |
| --- | --- | --- | --- |
| **S**ingle responsibility | Partial | One class still mixes argv shapes | Strategy per mode; shared wipe/cohesion kernel |
| **O**pen/closed | Weak | Mode via if/elif soup would grow `MeasureRun` | `MeasureMode` + polymorphic runners (decision 13) |
| **L**iskov | OK if | Climb must not pretend to be oracle | Climb refuses whole-repo fail_under claim |
| **I**nterface segregation | Partial | Fat CLI args | Thin facade; scope only on climb |
| **D**ependency inversion | Partial | Hardcoded pytest argv | Port/protocol; pytest-cov argv builder as adapter |
| **DRY** | Risk | Sharing fail_under flag looks “DRY” but couples predicates | **Wrong abstraction** (Metz): shared flag across modes is the bug |
| **OCP** | Need 13 | Extending modes must not edit a boolean labyrinth | Register strategies; no mode-boolean soup (15) |

**DRY corrected:** share PathCohesionGuard, wipe, report loaders — **not**
`--cov-fail-under=98.7` across modes. Identical flag, different measured
source set = false DRY.

---

## 5. complexipy ≤5 and naming

| Gate | Today | Dual-mode rule |
| --- | --- | --- |
| Cognitive complexity ≤5 | Hard fail via complexipy `[Confirmed]` CONTRIBUTING / ratchets | Mode dispatch must not introduce nested mode-boolean soup (decision 15) |
| Size ≤225 LOC | Hard fail; `cli.py` already over budget | Thin facades only; no utils dump (decision 10) |
| Naming | Domain modules (`coverage_measure`, `coverage_path_cohesion`, …) | No single-letter locals/params for modes (`m`/`o`/`c`); use `MeasureMode.ORACLE` / `CLIMB`, `scope_package`, `fail_under_floor` (decision 14) |

Hofmeister et al. / Clean Code (secondary culture): shorter identifiers
slow comprehension — refuse abbreviation theater in measure code paths.
Semantic-density papers (arXiv:2604.07502, 2604.17659) `[Evidenced]` in
taxonomy memo — prefer descriptive names over token compression.

---

## 6. Embody / Adopt / Refuse (segment 01 scope)

**Legend:** Embody = already true here · Adopt = take next (design→impl) ·
Refuse = wrong shape for this product.

| Item | Stance | Why |
| --- | --- | --- |
| Oracle = whole-repo SoT / SLO-like floor | **Embody** (policy) / **Adopt** (explicit `--mode oracle`) | Already CI + MeasureRun; need labeled default mode |
| Climb = scoped `--cov` accelerator | **Adopt** | CoverUp-shaped inner loop; wall-clock win |
| Scoped Cover% as proof of 98.7 | **Refuse** | pytest-cov source override; different predicate |
| Climb applying whole-repo `fail_under` | **Refuse** | Hidden SoT; false green |
| Gap-average as targeting SoT rewrite | **Refuse** | Derived view only; rebuild from oracle XML |
| diff-cover as below-floor climb driver | **Refuse** (as primary) | Wrong granularity; keep as new-code gate (**Embody**) |
| PathCohesion + single-writer wipe | **Embody** | Keep for both modes |
| Cross-worktree combine / `[paths]` rescue | **Refuse** | coveragepy pathmap risk; contradicts landed contract |
| xdist on climb in v1 | **Refuse (defer)** | Optional later; more combine surface before mode split |
| Strategy/polymorphism for modes | **Adopt** | OCP; complexipy ≤5 |
| Single-letter mode vars | **Refuse** | Decision 14 |
| Weakening CI 98.7 / cov on 3.10+3.12 | **Refuse** | Matrix already correct |
| LLM-as-judge as fail_under | **Refuse** | Taxonomy segment; deterministic gates only |
| ChaCo-style PR patch focus as climb SoT | **Refuse** | Orthogonal; use diff-cover for new code |
| Distinct climb artifact path vs refuse `coverage.xml` write | **Adopt (choose one)** | Decision 16 product choice — still `[Unknown]` which option |

---

## 7. Amended decision bullets (approve set for dual-mode)

Prior design memo **1–12** remain the dual-mode skeleton. This segment
**amends** with quality-bar **13–16** (required before implement). Align
with taxonomy **17–24** when synthesizing; do not approve 1–12 alone.

### Keep (1–12) — restated tightly

1. **One entry point:** `doc-engine coverage-measure --mode oracle|climb`
   (default `oracle`); not a second top-level command.
2. **Climb scope:** `--scope <package>` → pytest `--cov=<scope>`; optional
   trailing pytest paths for suite narrowing.
3. **Climb must not apply whole-repo `fail_under=98.7`.** Optional later
   `--climb-floor` = local advisory only, never CI SoT.
4. **Gap inventory** stays derived from last cohesive **oracle** XML;
   climb does not rewrite targeting SoT.
5. **Oracle cadence (docs):** remesure after climb batch / before PR /
   when inventory stale — not every file edit.
6. **PathCohesionGuard + wipe** for both modes; forbid cross-worktree
   combine.
7. **Do not weaken CI 98.7** on 3.11; do not add cov cells on 3.10/3.12.
8. **xdist:** out of v1; optional climb-only follow-up.
9. **diff-cover:** unchanged new-code gate; not climb inventory.
10. **CLI thin facade;** split parsers if still >225 LOC — no utils bag.
11. **Banner:** climb stderr must say `mode=climb (not CI oracle)`.
12. **Land on wave1 tip** that already owns MeasureRun/PathCohesion —
    not a SoT-forking side branch.

### Amend — required (13–16)

13. **OCP / polymorphism:** introduce `MeasureMode.ORACLE | CLIMB` (or
    equivalent strategies) sharing wipe + PathCohesion; **no** growing
    if/elif god in `MeasureRun.execute`. Hexagonal: argv builder as
    adapter behind a small port.
14. **Naming bar:** domain vocabulary only — `measure_mode`,
    `scope_package`, `oracle_fail_under`; **refuse** single-letter mode
    flags (`m`/`o`/`c`) and unexplained abbreviations in new measure code.
15. **complexipy ≤5:** mode dispatch and argv construction must stay
    within cognitive ≤5; extract helpers rather than boolean soup. Size
    ratchet ≤225 still binds new modules.
16. **DDIA promotion ban + artifact policy:** climb artifacts must not
    silently promote to oracle SoR. **Record one product choice before
    impl:** (A) climb writes a distinct path (e.g. `coverage-climb.xml`)
    **or** (B) climb refuses to write `coverage.xml` and prints scope
    Cover% only. Banner alone is insufficient if the filename collides.

### Cross-link (not owned by this segment)

Taxonomy decisions **17–24** (layer binding, no ungated self-evolution,
LLM-judge ≠ fail_under, SDD one-stream, framework refuse list, Green-Ops,
semantic density) remain in
[`docs/agentic-foundational-se-taxonomy-2026-08-08.md`](../agentic-foundational-se-taxonomy-2026-08-08.md).
Synthesis coordinator merges after siblings 02–05 land.

---

## 8. Principle scorecard (after amendments)

| Concern | Before (1–12 only) | After (+13–16) |
| --- | --- | --- |
| DDIA SoR vs derived | Partial | Pass if 16 chooses A or B |
| SOLID / OCP | Partial | Pass with 13 |
| DRY (correct abstraction) | Fail risk (shared fail_under) | Pass with 3 + 16 |
| complexipy ≤5 | Gap | Pass with 15 |
| Naming | Gap | Pass with 14 |
| Scoped cov ≠ fail_under | Stated in prose | Enforce via 3, 11, 16 |

---

## 9. Verdict

**Safe to approve decisions 1–12 alone?** No.

**Amend then approve:** Yes — approve **1–16** together (and acknowledge
taxonomy 17–21 as process constraints for the impl PR). Minimum bar:

1. Strategy + naming + complexipy ≤5 (13–15).
2. Promotion ban + explicit climb artifact policy A or B (16).
3. Scoped climb never claims whole-repo floor (3, 11).
4. No CI floor weaken; PathCohesion retained (6, 7).

**Implementation:** out of scope for this research segment. No dual-mode
code in this commit.

**Sibling coordination:** only this path
`docs/research/01-coverage-oracle-climb-solid.md` is authored here.
WIP dump / synthesis / taxonomy / design memo updates belong to the
coordinator after siblings land.

---

## 10. References (anchors)

- CoverUp — https://arxiv.org/abs/2403.16218
- ChaCo — https://arxiv.org/abs/2601.10942
- pytest-cov config — https://pytest-cov.readthedocs.io/en/latest/config.html
- pytest-cov#528 — https://github.com/pytest-dev/pytest-cov/issues/528
- DeepWiki pytest-cov controllers — https://deepwiki.com/pytest-dev/pytest-cov/2.2-coverage-controllers-and-execution-modes
- Local SoR playbook — `docs/design/ddia-north-star/playbooks/choosing-sor-vs-view.md`
- Design memo (1–12) — `docs/design/coverage-measure-modes-design-2026-08-08.md`
- Seams — `src/doc_engine/ci/coverage_measure.py`, PathCohesionGuard, CONTRIBUTING coverage table

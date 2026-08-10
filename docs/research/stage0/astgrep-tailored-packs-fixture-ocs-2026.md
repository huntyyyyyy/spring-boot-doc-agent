---
title: E-AST0 — Tailored ast-grep packs (fixture Stage-0 + OCS campaign + Python vacuity)
status: DRAFT — Spec gate E-AST0 (research complete; do not implement pack migration until Approve)
research date: 2026-08-10
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine + spring-signals dual plant
related:
  - docs/research/ci/36-ocs-dual-plant-profile-2026.md
  - docs/research/modularity/16-scan1-astgrep-modularity-2026.md
  - docs/research/coverage-quality/33-rust-quality-toolscape-bfs-dfs-2026.md
  - docs/research/process/35-control-plane-closed-loop-2026.md
  - spring-signals/docs/CAMPAIGN.md
  - spring-signals/docs/RULE_ID_MIGRATION.md
  - src/doc_engine/scanning/resources/spring_ast_grep_rules.yml
do_not:
  - make Artifactory OCS CodeQL DB the merge SoT
  - treat bare ripgrep hits as citation/SoT for Spring or vacuity
  - in-tree Rust rewrite; swap to ast-grep-py
  - land wave-1 id rename without coordinated fixtures + rule_coverage
  - soft-green empty OCS floors as "no expectation yet"
spec_gate: DRAFT E-AST0 — AST0-A–H below; Approve before Implement
---

# Principal memo: repo- and OCS-tailored ast-grep customizations

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Keep building ast-grep while researching? | **Yes.** Pin stays `ast-grep-cli~=0.45.0` (Embody). Add **named packs**, not one god YAML. |
| One rule file for everything? | **Refuse.** Split **Stage-0 Spring (fixture CI)** · **OCS campaign overlay** · **Python vacuity** — shared **utils** only. |
| What is broken today? | Stage-0 YAML still speaks **v0 ids** (`api_surface__mapping`, `raw_queries__query`, …) while CodeQL wave-1 / `fixture-repo.json` / OCS floors speak **migrated ids** (`api_surface__endpoint`, `sql__*`, `persistence__repository_marker`, …). `[Confirmed]` |
| OCS-specific customizations that earn their keep? | (1) class- vs method-level mapping split, (2) `BookBasedRepository` marker, (3) `javax.*` pending-import shape, (4) Messaging≡0 invariant as structural absence, (5) `files`/`ignores` main-vs-test. |
| Ripgrep role? | **Triage / learning ledger only** — never sole fail-closed SoT (citation mandate + industry move to tree-sitter oracles). |
| `vacuous` crate? | **Adopt** as certain-confidence Python vehicle (`~=0.1.2`, ★1 — pin exception like complexipy); **Embody** repo-local ast-grep rules for shapes we own. |
| DeepWiki? | **Unknown** this run (no DeepWiki MCP). Primaries: ast-grep docs + CAMPAIGN + tip YAML. |

**Bottom line:** Tailoring is not “more patterns.” It is **pack boundaries + relational idioms + vocabulary sync + plant-scoped floors**, so fixture CI stays hermetic while OCS campaign rules measure the shapes that actually dominate `ocs-api-service` @ develop (Spring Boot 2.7 / `javax.*` / marker repositories / fat ApiSurface).

**Constitution (do not soften):** fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` grab-bag in *Python* (YAML `utilDirs` are ast-grep utilities, not a Python package) · policy **16-A** · fixture = CodeQL merge SoR (E-OCS0) · Spec → Implement → Verify → Archive.

---

## 1. Frame and alternatives

### Question

What ast-grep **project layout, utils, relational patterns, rule ids, and plant-scoped customizations** should this product Embody so that (a) Stage-0 on hermetic fixtures stays honest, and (b) offline/campaign measurement against `ocs-api-service @ develop` improves recall without making Artifactory CodeQL the merge SoT?

### Alternatives considered

| Option | Verdict |
| --- | --- |
| A. Keep single `spring_ast_grep_rules.yml`; grow forever | **Refuse** — vocabulary and plant concerns already diverge; LOC/comment debt already high |
| B. `sgconfig.yml` + `ruleDirs` / `utilDirs` packs (Spring fixture, OCS overlay, Python vacuity) | **Adopt** Spec-gated |
| C. Replace Stage-0 with CodeQL-only on OCS | **Refuse** — non-hermetic; E-OCS0 OCS1/OCS7 |
| D. Bare `rg` for Spring annotations / `assert True` | **Refuse** as SoT; **Adopt** as triage sensor |
| E. In-tree Rust scanners | **Refuse** (Embody wheels only) |
| F. Copy wave-1 QL ids into ast-grep in one tip without fixtures | **Refuse** — CAMPAIGN landing mode B; `rule_coverage` fails |

---

## 2. Evidence (tiered)

### 2.1 Evidenced (primary docs / crates)

| Claim | Source |
| --- | --- |
| Project scans need `sgconfig.yml` with `ruleDirs`; optional `utilDirs` + `matches` for reusable sub-rules | [ast-grep project config](https://ast-grep.github.io/guide/project/project-config.html), [sgconfig reference](https://ast-grep.github.io/reference/sgconfig.html), [utility rules](https://ast-grep.github.io/guide/rule-config/utility-rule.html) |
| Relational `has` / `inside` + `stopBy: end` is the supported way to survive annotation adjacency | [Relational rules](https://ast-grep.github.io/guide/rule-config/relational-rule.html) |
| Per-rule `files` / `ignores` globs scope application (paths relative to project root; no `./` prefix) | [YAML config reference](https://ast-grep.github.io/reference/yaml.html) |
| Tree-sitter static vacuity for Python tests (`no-assertions`, `constant-assertion`, …) with `certain`/`likely` | [vacuous 0.1.2](https://pypi.org/project/vacuous/) / [MahdiAlani/vacuous](https://github.com/MahdiAlani/vacuous) (★1 as of 2026-08-10) |
| Structural/oracle preference over grep for agent correctness | Codebase-Memory [arXiv:2603.27277](https://arxiv.org/abs/2603.27277); this repo’s CLAUDE.md citation mandate |
| ast-grep still active upstream | GitHub `ast-grep/ast-grep` ★15457, pushed 2026-08-09 |

### 2.2 Confirmed (this tip)

| Fact | Where |
| --- | --- |
| Stage-0 shipfile: 29 Java rules, id shape `bucket__subkind`, loaded via `ast-grep scan -r … --json=compact` (no `sgconfig.yml` today) | `src/doc_engine/scanning/resources/spring_ast_grep_rules.yml` |
| Relational rewrite already landed for `@Entity` / Spring Data repository roots after literal patterns died on annotation adjacency — verified on a large production Spring tree | YAML header comments + `persistence__entity` / `persistence__repository` |
| Always pair bare `@Name` and `@Name($$$)` for argument-bearing annotations | CLAUDE.md + mapping rules |
| Wave-1 vocabulary migration documents splits: `api_surface__mapping` → `path_prefix` + `endpoint`; `raw_queries__query` → `sql__*`; adds `persistence__repository_marker`, Jakarta/OpenAPI/Hibernate ids | `spring-signals/docs/RULE_ID_MIGRATION.md` |
| Stage-0 YAML + `rule_coverage_baseline.json` still emit **v0** ids (`api_surface__mapping`: 414 on external corpus) | tip baseline + YAML |
| Fixture expectations already use **wave-1** ids; OCS expectations pin ApiSurface floors (49/369/35) + `persistence__repository_marker`: 4 + Messaging asserted 0 | `harness/expectations/*.json` |
| OCS plant profile: fixture = merge SoR; OCS = campaign; offline ast-grep floor remeasure allowed without Artifactory | E-OCS0 / `docs/research/ci/36-ocs-dual-plant-profile-2026.md` |
| OCS checkout **absent** on this cloud VM (`DOC_ENGINE_REAL_REPO` unset) — live remeasure blocked; research uses CAMPAIGN + expectation notes | environment |
| Python vacuity hybrid gate in progress: `src/doc_engine/ci/vacuity/` (ast-grep rules + vacuous crate + rg triage + telemetry ledger) | tip WIP |
| Annotation-only / meta-resolution hole: fail-closed `isOrMeta(...Controller)` dropped all `@RestController` on OCS until both stereotypes enumerated | CAMPAIGN.md regression note |

### 2.3 Unknown

| Item | Why |
| --- | --- |
| Exact live hit counts for proposed OCS overlay rules on tip machine | No `ocs-api-service` checkout |
| Whether CodeQL wave-1 packs are fully merged vs still campaign-local | Partially Confirmed via docs; pack tip state not re-audited this pass |
| DeepWiki cartography of ast-grep org | MCP unavailable this run |
| Optimal `utilDirs` granularity (one util per annotation family vs per plant) | Product choice — lock at Spec Approve |

---

## 3. What “tailored to this repo + OCS” actually means

Three **products** share one engine; they do not share one YAML:

```text
sgconfig.yml                    # Adopt — project root or pack-root
  ruleDirs:
    - rules/spring_stage0       # hermetic CI / Stage-0 (fixture SoR sibling)
    - rules/python_vacuity      # doc-engine tests fail-closed
    - rules/ocs_overlay         # campaign-only; never required for merge CI
  utilDirs:
    - utils/spring_java         # shared: is_marker_annotation, is_mapping_anno, …
```

| Pack | Language | Plant | Fail-closed where? |
| --- | --- | --- | --- |
| `spring_stage0` | Java | fixture | Stage-0 scan + `rule_coverage` fixtures |
| `ocs_overlay` | Java | ocs campaign / offline remeasure | Operator floors in `ocs-api-service.json` — **not** GitHub merge job |
| `python_vacuity` | Python | doc-engine tip | `pre_pr` hard suite `vacuous_tests` |

**Python package rule still holds:** no `src/.../utils/` grab-bag. ast-grep’s `utilDirs` are YAML utilities referenced via `matches:` — different namespace.

---

## 4. Customization catalog (Embody / Adopt / Refuse)

### 4.1 Idioms already earned (Embody — keep teaching every new rule)

1. **Relational over literal adjacency** for type-level stereotypes (`kind: class_declaration` + `has: marker_annotation` + `stopBy: end`).
2. **Dual forms** for annotations that take arguments: `@GetMapping` **and** `@GetMapping($$$ARGS)`.
3. **Regex on matched node text in Python**, never whole-file regex, for NAME/TABLE/ENTITY extraction.
4. **Zero match ≠ absence** — unproven until pattern validated on playground + fixture.
5. **Id shape** `bucket__subkind` with stable buckets for evidence maps.

### 4.2 OCS-shaped rules to Adopt (campaign overlay / floor remeasure)

Measured shapes from CAMPAIGN + `ocs-api-service.json` notes (596 `.java`, 420 main / 176 test; SB 2.7.18; `javax.*`):

| Customization | Why OCS-specific | Proposed ast-grep shape (sketch) | SoT role |
| --- | --- | --- | --- |
| **A. Mapping split** | Floors: 369 method shortcuts + 35 class-level `@RequestMapping` path prefixes — Stage-0’s single `api_surface__mapping` cannot assert either floor | Two rules: method-level `*_Mapping` **inside** `method_declaration`; class-level `@RequestMapping` **inside** `class_declaration` / `interface_declaration` → ids `api_surface__endpoint` / `api_surface__path_prefix` | Align Stage-0 vocabulary (migration B) **or** dual-emit adapter until B lands |
| **B. Controller meta** | `@RestController` ⊕ `@Controller` = 49; meta-or that only names Controller is a silent recall hole | Explicit `any:` of both markers (Embody CAMPAIGN lesson); util `is_spring_web_controller` | Fixture + OCS floors |
| **C. Repository marker** | Four interfaces extend empty `BookBasedRepository` — not a Spring Data root; CodeQL id `persistence__repository_marker` | `interface_declaration` + `has` extends `type_identifier` regex `BookBasedRepository` (parameterize via util / plant config later) | OCS overlay + fixture sample; **not** generic Stage-0 without a fixture twin |
| **D. Spring Data roots** | Keep relational extends of `JpaRepository|CrudRepository|…` | Existing `persistence__repository` | Stage-0 |
| **E. Jakarta pending** | ~297 `jakarta__pending_import` (javax.persistence heavy) on OCS burndown | `import_declaration` regex `^import javax\.(persistence|validation|annotation|servlet)\.` → pending ids; twin for `jakarta.` → migrated | OCS overlay + fixture javax samples; generation axis as **bucket**, not SpringBoot-only column |
| **F. Messaging ≡ 0** | Asserted empty: no kafka/rabbit/… on classpath | Absence is **expectation asserted rows=0**, not an ast-grep “match nothing” claim. Optional positive rules for `@KafkaListener` etc. stay Stage-0; OCS asserts zero hits | Assertion engine (already) |
| **G. OpenAPI generation** | swagger2 ~148 vs openapi3 ~1012 | Separate rules / utils for `io.swagger` vs `io.swagger.v3` / `org.springdoc` | Campaign first; Stage-0 fixtures for both |
| **H. Native SQL** | `@Query(nativeQuery=true)` + JDBC | Prefer structured `@Query($$$ARGS)` + Python `nativeQuery` parse (today) → migrate id to `sql__data_query_native` with fixtures | Coordinated with RULE_ID_MIGRATION |
| **I. `files` globs** | Main vs test density differs (420/176) | `files: ["**/src/main/java/**/*.java"]` on production stereotypes; testing rules scoped to `**/src/test/java/**` | Reduces FP and floor noise |
| **J. Row-visibility Hibernate** | JPA survey: `@SQLRestriction` / `@Filter` / `@SoftDelete` change rows not tables | Optional overlay rules — **Defer** until Persistence floors exist for OCS (expectation placeholders only today) | Research backlog, not E-AST0 MVP |

### 4.3 Python vacuity pack (this repo’s control plane)

| Layer | Role | Stance |
| --- | --- | --- |
| ast-grep rules (`assert True`, `test_*` body only `pass`/`...`) | Repo-owned structural shapes | **Embody** in `python_vacuity` |
| `vacuous check --min-confidence certain` | Broader tree-sitter checks (swallowed failure, etc.) | **Adopt** pinned wheel |
| ripgrep triage | Candidate ledger for learning | **Adopt sensor** only |
| Empty hard-suite telemetry | Observation vacuity | **Embody** (already in `pre_pr`) |

Intentional meta-fixtures that *demonstrate* vacuity must live under `scripts/fixtures/vacuity/`, not under collected `tests/ci` bodies — otherwise the gate fights the teacher.

### 4.4 Explicit Refuse

- OCS CodeQL DB create as CI merge SoT without Artifactory hermeticity.
- Softening OCS floors when overlay rules are missing (“no expectation yet” ≠ green proof).
- Text-search-only claims that an annotation is absent.
- Expanding Stage-0 denominator with OCS-only rule ids before fixture twins exist (`rule_coverage` contract).
- `sgconfig` that points campaign overlays into the GitHub `codeql-signals` / Stage-0 merge path.

---

## 5. Spec decisions (AST0-A–H) — DRAFT

| ID | Decision | Status |
| --- | --- | --- |
| **AST0-A** | Three packs: `spring_stage0`, `ocs_overlay`, `python_vacuity`; optional root `sgconfig.yml` with `ruleDirs`/`utilDirs` | DRAFT |
| **AST0-B** | Vocabulary: either (B1) migrate Stage-0 YAML + fixtures + baseline to wave-1 ids in one epic tip, or (B2) dual-emit adapter mapping v0→v1 for floors — pick at Approve; default lean **B1** with CAMPAIGN landing mode B | DRAFT |
| **AST0-C** | OCS overlay may reference plant-local type names (`BookBasedRepository`) behind a config/util; never hardcode client names into hermetic Stage-0 without fixture twin | DRAFT |
| **AST0-D** | Offline `remeasure_ocs_floors.py` consumes **ast-grep packs only** when Artifactory absent; writes proposal JSON for operator review (E-OCS0 OCS6) | DRAFT |
| **AST0-E** | Hybrid vacuity hard gate: ast-grep ∪ vacuous(`certain`) ∪ empty telemetry; rg ledger-only | DRAFT (impl in flight on tip) |
| **AST0-F** | Utils for Spring: `is_rest_controller`, `is_request_mapping`, `is_spring_data_repo_root`, `is_javax_persistence_import` — referenced via `matches` | DRAFT |
| **AST0-G** | Merge CI continues fingerprint-gated fixture CodeQL; OCS overlay never required for green main | DRAFT (= OCS7) |
| **AST0-H** | Refuse in-tree Rust / ast-grep-py / rg-as-SoT / raising constitution gates | DRAFT |

**Approve gate:** product owner locks AST0-B (B1 vs B2) and whether `BookBasedRepository` is parameterized vs duplicated fixture marker name.

---

## 6. Adversarial checklist

- [ ] Vocabulary rename without fixture/`rule_coverage` same-PR → CI red or silent denominator lie
- [ ] Overlay rule without `files:` includes test doubles → floor inflation
- [ ] Literal `@Entity\npublic class` revival → adjacency FP/FN on OCS
- [ ] Meta-or Controller without RestController → OCS recall cliff (already bitten)
- [ ] Claiming Messaging absent from a zero ast-grep match without expectation asserted-0
- [ ] Vacuity gate scanning intentional teacher fixtures under `tests/`
- [ ] Treating ★1 `vacuous` as ≥10k SoR myth — pin as vehicle, keep repo rules
- [ ] Dual plant soft-green when checkout or Artifactory missing

---

## 7. Epic sketch (fresh-chat ready) — after Spec Approve

**Epic goal:** Ship tailored ast-grep packs so fixture Stage-0 and OCS campaign floors share idioms but not SoT, and Python vacuity stays fail-closed.

| Ticket | Title | Acceptance |
| --- | --- | --- |
| AST0-1 | Spec Approve AST0-A–H (lock B1/B2) | Frontmatter `APPROVED`; design memo status flipped |
| AST0-2 | `sgconfig` + utilDirs scaffold (no id rename yet) | `ast-grep scan --config …` loads stage0; tests green |
| AST0-3 | Python vacuity pack + hard `pre_pr` suite | Planted `assert True` / empty hard log fails; tip clean |
| AST0-4 | Mapping split rules + fixture twins (if B1) | Floors path_prefix/endpoint assertable on fixture-repo |
| AST0-5 | OCS overlay: marker repo + javax pending + globs | Dry-run remeasure proposes deltas when checkout present |
| AST0-6 | Archive: CAMPAIGN + CONSTRAINTS + backlog P-line | Claims checker clean if scripts/skills touched |

**Spikes**

| Spike | Exit |
| --- | --- |
| S-AST0-1 Live OCS overlay counts on work VPN checkout | Table of rule_id → count vs `ocs-api-service.json` floors; FN list |
| S-AST0-2 Dual-emit vs hard rename cost | LOC + ratchet impact estimate; pick B1/B2 |

**Exit:** Approved Spec + vacuity hard gate on tip + (B1 or B2) vocabulary plan executed for Stage-0 **or** explicitly deferred with adapter tests; OCS overlay documented as campaign-only.

---

## 8. Parallel build note (this tip)

While Spec stays DRAFT for pack migration, **continue** the hybrid vacuity pack (`src/doc_engine/ci/vacuity/`) — it is pack `python_vacuity` MVP and does not require OCS checkout. Do **not** rename `spring_ast_grep_rules.yml` ids on this tip without AST0-1 Approve.

---

## Invariants

fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no Python `utils/` · ast-grep Embody · fixture CodeQL merge SoR · OCS campaign fail-closed without credentials · Spec → Implement → Verify → Archive

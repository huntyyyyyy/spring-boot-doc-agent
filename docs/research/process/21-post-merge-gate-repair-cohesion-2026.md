---
title: E-HOT0 — Post-merge CI red vs cohesion (gate repair Spec)
status: DRAFT Spec — pending Approve of HOT1–HOT13
research date: 2026-08-09
research_window: 2026-06-01 → 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI modular monolith (`doc_engine` + `stf`) — main red after #112 merge
related:
  - docs/research/findings/2026-08-09-statement-split-cascade.md
  - docs/design/concept-split-cohesion-design-2026-08-09.md
  - docs/research/modularity/20-tach-dependency-blueprint-2026.md
  - docs/research/process/14-facade-poke-research-hooks-2026.md
  - docs/research/process/19-watch-stalker-agents-context-lean-2026.md
  - docs/research/process/22-stack-rescope-10k-star-bar-2026.md
  - docs/research/quality-backlog.md
  - scripts/ci/pre_pr.py
do_not:
  - resume mechanical LOC/statement thrash to “clear” red (fails E-COH0)
  - weaken fail_under 98.7 / complexipy≤5 / LOC≤225 / statements≤20
  - treat façade private-re-export warehouse as finished modularity
  - Approve E-TACH0 depends_on in the same tip as gate hotfix
  - start full E-STK1 Implement without Active switch (sensors Spec-ready only)
  - push before local `pre_pr --full` / oracle cell green
spec_gate: DRAFT E-HOT0 (2026-08-09) — HOT1–HOT13 pending Approve
gh_sor_bar: "≥10000★ and pushed_at within research_window (prefer Releases/CHANGELOG); in-repo Confirmed pins exempt from ★ for Embody-continue"
bar_raise: "2026-08-09 human: raise from ≥1000★ to ≥10000★ (+10k) for external implement SoR on this stream"
stack_rescope: "docs/research/process/22-stack-rescope-10k-star-bar-2026.md (E-STACK0 DRAFT)"
---

# Principal memo: post-merge gate repair under cohesion + 2026 modularity

**Question.** After merging tip `#112` despite red CI, how should this repo remediate
failures on `cursor/local-ci-gate-fix-61f3` while embodying principal-SE cohesion,
modern modularity frameworks (tach interfaces / ports), and local-CI-first discipline
— without repeating the statement-split cascade?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

**Research window:** 2026-06-01 → 2026-08-09.

**GitHub implement SoR bar (this stream):** **≥10,000★** and `pushed_at` in window
(human raise from the prior ≥1k★ bar — “10k more stars”). Star/push alone never
implies Adopt. **Exception:** tools already **Confirmed** pinned + CI-gated in this
repo may continue to **Embody** without clearing 10k★; they cannot be cited as
*new* external Adopt proof under this bar.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Is “just fix the red tests” Spec-shaped? | **Yes.** Failures span gate-policy scope, façade DIP seams, and provisional statement chops — not typos. `[Confirmed]` |
| Active stream conflict? | **E-COH1** reshape is Active; **COH1** already carves **hotfix for broken imports/CI**. Gate repair is that carve-out — Spec it as **E-HOT0**, then Implement as a **bounded hotfix epic**, then resume E-COH1 reshape. Do not invent a second tip writer. `[Confirmed]` design memo §4 |
| Primary repair pattern for G2? | **Return → unpack → pass** between `*_prelude` / `*_core` siblings (already used on ~19/23 pairs). Refuse merge-to-utils and refuse more mechanical chops. `[Confirmed]` AST inventory |
| CQ hard-scope vs unit tests? | Flat keys (`mod.py::f`) from scripts-only measure mode currently **escape** `_hard_statement_scope` (`src/`/`tests/` only) — tests wrote under `scripts/` and assert hard-fail. Spec must pick **A** (treat slash-free keys as in-scope) **or** **B** (retarget fixtures to `src/`/`tests/` trees). Prefer **A** as Verify of the product predicate; **B** alone hides the unit-test contract. `[Confirmed]` |
| Soft advisory when `FN_STMTS_SOFT == HARD`? | Soft band for functions collapsed; advisories fire only at `stmts == HARD`. Update characterization tests — do **not** re-open a soft band without Spec. `[Confirmed]` |
| Certification `str.value`? | Test patches façade alias; call site binds the **concept module** name. Patch where used (`certification_finish.build_and_write_certification`). Do not teach fold to accept bare strings as primary API. `[Evidenced]` pytest monkeypatch doctrine + `[Confirmed]` tip |
| Metamorphic wrap ratchet? | Failure message already says defect fixed — **delete ratchet** and fold transform into the invariant loop (test docstring SoT). `[Confirmed]` |
| Docs path pin? | Prompt live under `docs/process/steering-prompts/` (E-DOC1). Retarget path pin only. `[Confirmed]` |
| Modern frameworks to Embody? | **≥10k★ SoR:** pytest (~14k), ruff (~49k), semgrep (~16k), Nx patterns (~29k). **tach (~2.8k) fails ★ bar** — continue **Embody** only as in-repo Confirmed pin (cycle gate); do **not** expand `depends_on`/`[[interfaces]]` from ★ claims. Ports/strategies + local `pre_pr` stay. Refuse DI/mesh/Spec Kit/LLM-as-fail_under. `[Evidenced]` + `[Confirmed]` |
| Push policy? | **Refuse push until local CI-equivalent green** (`pre_pr --full` or oracle 3.11 cell). Remote Actions is witness, not discovery. `[Confirmed]` user mandate |

---

## 1. Problem frame

### 1.1 Sequence (Confirmed)

1. Mechanical statement chops (`HARD_STATEMENTS≤20`) without cohesion bar → G2–G6 cascade
   ([finding ledger](../findings/2026-08-09-statement-split-cascade.md)).
2. Tip `#112` merged to `main` **with failures** (explicit human request).
3. Follow-up branch `cursor/local-ci-gate-fix-61f3` at `main`; other `cursor/*` deleted.
4. Local re-run of suspected suites (2026-08-09): **9 failed, 21 errors** on the
   focused set (drift harness setup NameErrors dominate).

### 1.2 Category errors to refuse

| Error | Why |
| --- | --- |
| More statement/LOC agents in parallel | Root of cascade; violates one tip writer + COH1 |
| Raise ceilings to green | Constitution refuse |
| Patch façade warehouse deeper (`_` re-exports`) as “modularity done” | COH4; tach `[[interfaces]]` would reject |
| Soften `_hard_statement_scope` to empty / grandfather scripts as product | G6 open debt must stay visible |
| Start E-TACH0 `depends_on` while gates red | Wrong epic order (COH6 / TACH4) |
| Treat climb Cover% or LLM-judge as proof gates are green | Constitution |

---

## 2. Tip failure taxonomy (Confirmed)

| ID | Class | Manifestation | Linked gap |
| --- | --- | --- | --- |
| F1 | `split_scope_break` | 4 prelude/core pairs leak locals (`original_*`, `generative`, `entry`/`tmp`/`result`, `report`) | G2 |
| F2 | `facade_patch_miss` | `test_write_certification_finish_uncertified` patches `support._build_and_write_certification`; finish calls in-module `build_and_write_certification` → real fold gets `profile="certified"` str → `.value` | G3 / FAC poke |
| F3 | `policy_scope_skew` | CQ unit tests hard-fail statements under flat/`scripts/` keys; production hard-scope is `src/`+`tests/` only | G6 |
| F4 | `soft_band_collapsed` | `FN_STMTS_SOFT == FN_STMTS_HARD == 20`; mid soft advisory assert false | policy Verify |
| F5 | `ratchet_obsolete` | `wrap_annotation_args` no longer moves evidence set | metamorphic SoT |
| F6 | `path_migrate_drift` | `claude/steering-prompts/10-…` → `docs/process/steering-prompts/10-…` | E-DOC1 |

**AST inventory (Confirmed, 2026-08-09):** 23 `*_prelude`/`*_core` pairs in-tree;
**4 broken** (prelude assigns Load’d names; no return; core params omit them);
19 already use return→pass.

Broken paths:

- `tests/support/drift_normalization/harness.py` — `original_extract`, `original_backend`
- `tests/doc_engine/test_pipeline_runner_stages.py` — `generative`
- `tests/doc_engine/test_spring_signal_scan_determinism_refs.py` — `tmp`, `result`, `entry` (+ likely `parse` ImportFrom leak — verify in Implement)
- `tests/doc_engine/test_gap_probe_ocs_real_world.py` — `report` (opt-in live; still G2)

---

## 3. Evidence inventory (tiers)

### 3.1 This repo (Confirmed)

| Claim | Source |
| --- | --- |
| E-COH0 Approved; E-COH1 Active; mechanical chops Never | `quality-backlog.md` P17; design memo |
| COH1 allows CI/import hotfix carve-out | design memo §4 COH1 |
| Façade poke incident class already documented | research 14 |
| G1–G6 sensor Spec ready; E-STK1 Deferred | research 19 §8.1; backlog P15.1 |
| Local SoT: `scripts/ci/pre_pr.py` | CONTRIBUTING / AGENTS.md |
| Statement hard-scope helper + G6 note | `scripts/ci/check_code_quality.py` `_hard_statement_scope` |
| Soft fn advisory == hard equality only | `doc_engine.ci.size_ratchet.soft_advisories` |

### 3.2 GitHub ★ snapshot (Evidenced, fetched 2026-08-09)

| Repo | ★ | Clears ≥10k★? | Role for E-HOT0 |
| --- | ---: | --- | --- |
| [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | 14397 | **Yes** | Monkeypatch / fixtures SoR for F2 + test intentionality |
| [astral-sh/ruff](https://github.com/astral-sh/ruff) | 49115 | **Yes** | Lint gate already Confirmed |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | 16162 | **Yes** | Stage-0 / rules already Confirmed |
| [nrwl/nx](https://github.com/nrwl/nx) | 29207 | **Yes** | **Pattern only** (module boundaries) — wrong runtime |
| [github/codeql](https://github.com/github/codeql) | 9923 | **No** (&lt;10k) | Keep as Confirmed in-repo use; not *new* Adopt via ★ |
| [tach-org/tach](https://github.com/tach-org/tach) | 2786 | **No** | **Confirmed pin only** — not external ★ SoR under raised bar |
| [seddonym/import-linter](https://github.com/seddonym/import-linter) | 1130 | **No** | Still Defer dual-gate; ★ worse under 10k bar |
| [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | 8856 | **No** | E-QA3 Spike stays Spike; not merge SoR via ★ |

### 3.3 Modern frameworks / primaries (Evidenced)

| Claim | Source | Stance for this product |
| --- | --- | --- |
| Patch **where the name is used**, not only where defined | [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) (≥10k★ host) | **Embody** for F2 |
| Enforced module edges + public interfaces | tach docs + research 20; **Nx** (≥10k★) as pattern analogue | **Embody** tach *cycles* as Confirmed pin; **Defer** depends_on/interfaces expansion; steal *patterns* from Nx not Nx runtime |
| Size/complexity reduction ≠ seam design | arXiv [2506.06764](https://arxiv.org/abs/2506.06764); [2402.05559](https://arxiv.org/abs/2402.05559) | **Adopt** “gates verify; do not design”; refuse auto-extract thrash |
| Semantic cohesion / task-scoped modularity | arXiv [2603.15690](https://arxiv.org/abs/2603.15690) | **Adopt** concept; **Refuse** LSS/MAS rewrite of CLI |
| Ports + characterization poke surfaces | research 12/14; pytest characterization culture (≥10k★) | **Embody** |

### 3.4 Unknown (must not invent)

| Item | Why Unknown |
| --- | --- |
| Full oracle cell wall-clock after F1–F6 only | Not measured this session |
| Whether more G2 pairs hide behind uncollected paths | AST covered `*.py`; live/skipped tests may still fail differently |
| Soft≠Hard restore for statements | Needs product Spec if desired — not assumed |
| E-STK1 sensor code shapes | Deferred; Spec sensors G1–G6 only |

---

## 4. Alternatives (weighed)

| Alt | Description | Verdict |
| --- | --- | --- |
| **H0** | Revert `#112` merge | Refuse — human chose merge-with-failures; tip content includes Approved Specs |
| **H1** | Hotfix F1–F6 under E-HOT Spec; local green; then resume E-COH1 reshape | **Prefer** |
| **H2** | Fold all fixes into deep E-COH1 reshape now | Refuse as first move — expands blast radius; gates still red |
| **H3** | Raise statement soft/hard or scope out tests | Refuse constitution |
| **H4** | Merge every prelude/core back into one function | Defer — only if return/pass cannot meet ≤20 **and** COH10 intentional split still fails; prefer return/pass first |
| **H5** | Implement E-STK1 sensors in same tip as hotfix | Refuse dual Active; sensors stay Spec inputs until Active switch |

---

## 5. Design principles for the hotfix (locked by Approve)

1. **Hotfix ≠ reshape.** Only restore broken contracts and align characterization with
   already-Approved policy. No new residual bins; no façade private warehouses.
2. **G2 default repair = explicit dataflow** (return/pass), matching repaired climb tests.
3. **Patch at the binding site** for characterization doubles; concept module remains enum SoT.
4. **CQ scope:** slash-free measure keys are in hard scope (unit / scripts-only mode);
   `scripts/**` repo-relative keys stay measured debt (G6), not silent product grandfather.
5. **Collapsed soft band:** update size helper tests to current equality semantics.
6. **Obsolete ratchets die** when their docstring says so — do not invert assert.
7. **Path pins follow E-DOC1** live locations under `docs/`.
8. **Verify locally first** — `pre_pr --full` (or documented oracle cell) before push.
9. **One tip writer** on `cursor/local-ci-gate-fix-61f3`.
10. **No E-TACH0 map edits** in the hotfix epic.
11. **E-STK1 remains Deferred**; optionally append finding notes only.
12. **After green:** Archive finding disposition; resume Active **E-COH1** inventory/reshape.

---

## 6. Spec decisions (HOT1–HOT12) — pending Approve

| ID | Decision |
| --- | --- |
| **HOT1** | Gate repair is the COH1 carve-out; Spec epic **E-HOT0** then Implement **E-HOT1**; Active tip stays one branch |
| **HOT2** | Repair all known G2 pairs with return→unpack→pass; include opt-in live pair |
| **HOT3** | Do not introduce `utils/` or residual `part2` modules for handoff |
| **HOT4** | Certification climb test patches `certification_finish.build_and_write_certification` (use site); fold keeps enum `.value` |
| **HOT5** | `_hard_statement_scope`: `True` for slash-free keys **or** keys under `src/`/`tests/`; `False` for `scripts/` repo-relative |
| **HOT6** | Size soft-advisory characterization matches `FN_STMTS_SOFT == HARD` (equality-only fn notes) |
| **HOT7** | Delete obsolete `wrap_annotation_args` moves-the-set ratchet; fold into formatting invariant loop |
| **HOT8** | Retarget `test_prompt_10_cites_north_star_path` to `docs/process/steering-prompts/10-…` |
| **HOT9** | Implement may not raise LOC/stmt/complexipy ceilings or fail_under |
| **HOT10** | Push forbidden until local full gate green; remote CI is witness |
| **HOT11** | No `tach.toml` depends_on/interfaces expansion in E-HOT1 |
| **HOT12** | On exit: update finding ledger disposition; set backlog Active back to **E-COH1** reshape (not E-STK1 unless human switches) |
| **HOT13** | External implement SoR for *new* frameworks/deps on this stream: **≥10,000★** + push in window; in-repo Confirmed pins (tach, CodeQL, …) may Embody-continue without ★; do not cite &lt;10k★ GH as *new* Adopt proof |

---

## 7. Epic sketch (fresh-chat ready)

### E-HOT0 — Spec gate (this memo)

- **Exit:** `spec_gate: APPROVED E-HOT0` + HOT1–HOT12 stamped; backlog P18.0 Approved.

### E-HOT1 — Implement gate repair

| ID | Title | Acceptance |
| --- | --- | --- |
| HOT1-1 | G2 return/pass on 4 broken pairs (+ `parse` if needed) | no NameError on drift/pipeline/scan/gap prelude paths |
| HOT1-2 | Cert finish monkeypatch at concept module | `test_write_certification_finish_uncertified` green; fold still enum |
| HOT1-3 | CQ scope HOT5 + ratchet tests green | `test_code_quality_ratchet` statement hard-fails |
| HOT1-4 | Size soft advisory test aligned | `test_hard_soft_and_compare_offenders` green |
| HOT1-5 | Metamorphic + prompt path | HOT7–HOT8 green |
| HOT1-6 | Local Verify | `pre_pr --full` exit 0 (or oracle cell + documented peers) before push |

**Spikes:** none required if AST inventory holds; optional Spike if full suite reveals new G2.

**Invariants:** constitution gates; COH2–COH4 on any touched product module; one tip writer.

### After E-HOT1

Resume **E-COH1** (COH1-1 inventory …) under cohesion bar. Keep E-STK1 / E-TACH0 / E-CQL1 Deferred unless Active switch.

---

## 8. Adversarial checklist

- [ ] Does Approve re-open LOC thrash? — **Forbidden (HOT9, COH1).**
- [ ] Does HOT5 grandfather `scripts/` product debt? — **No;** measured, not hard-failed.
- [ ] Does F2 fix weaken enum boundary? — **No;** patch use-site only.
- [ ] Does hotfix edit tach map? — **No (HOT11).**
- [ ] Parallel E-STK1 Implement? — **No (HOT12).**
- [ ] Push on red local? — **No (HOT10).**
- [ ] Is return/pass a residual bin? — **No;** same concept module, explicit dataflow.
- [ ] Are metamorphic asserts inverted to keep a dead defect? — **No (HOT7).**

---

## 9. Embody / Adopt / Refuse (product)

| Stance | Item |
| --- | --- |
| **Embody** | Local `pre_pr` before push; G2 explicit dataflow; patch-at-use (pytest ≥10k★ doctrine); tach **cycle** gate as Confirmed pin; finding ledger |
| **Adopt** | HOT epic as COH1 carve-out; CQ slash-free hard scope; delete fixed ratchets; docs path pins; **≥10k★** bar for *new* external SoR (HOT13); Nx-style boundary *patterns* only |
| **Defer** | E-STK1 sensors code; E-TACH0 depends_on/`[[interfaces]]` (tach fails 10k★ — needs Confirmed+Approve, not ★); soft≠hard statement band; deep E-COH1 reshape until green; global synthesis rewrite of older ≥1k★ memos |
| **Refuse** | Ceiling raises; utils bags; façade private warehouses; LLM/Cover% as green proof; parallel tip thrash; **new** Adopt of &lt;10k★ GH trees as implement SoR on this stream |

---

## 10. Exit

**E-HOT0 remains DRAFT until human Approve of HOT1–HOT13.**
No product Implement on this stream until Approve is recorded in this memo + backlog.

**Note on bar raise:** Older memos (E-STK0 / E-TACH0) still say ≥1k★. Raising the
*repo-wide* default is a synthesis decision — out of scope for E-HOT1 code.
This stream locks **≥10k★** for its own external SoR (HOT13) immediately on Approve.

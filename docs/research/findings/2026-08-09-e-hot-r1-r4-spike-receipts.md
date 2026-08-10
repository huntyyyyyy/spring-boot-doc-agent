---
title: E-HOT-R1–R4 spike receipts — gate repair benchmarks (2026-08-09)
status: complete
kind: research_spike
date: '2026-08-09'
related:
- docs/research/process/21-post-merge-gate-repair-cohesion-2026.md
- docs/research/findings/2026-08-09-statement-split-cascade.md
- docs/design/post-merge-gate-repair-design-2026-08-09.md
epics: E-HOT-R1, E-HOT-R2, E-HOT-R3, E-HOT-R4
claim_tiers: Evidenced / Confirmed / Unknown
last_reviewed: '2026-08-10'
---

# Spike receipts: E-HOT-R1–R4 (before E-HOT1 Implement)

## E-HOT-R1 — G2 repair benchmark `[Confirmed]`

| Metric | Value |
| --- | --- |
| prelude/core pairs | 23 |
| broken (leaked Locals) | **4** |
| healthy | 19 |
| Max pre/core stmts among broken | 16 / 14 (under HARD 20) |

**Broken inventory**

| Path | Leaked | Choice |
| --- | --- | --- |
| `tests/support/drift_normalization/harness.py` | `original_extract`, `original_backend` | return/pass |
| `tests/doc_engine/test_pipeline_runner_stages.py` | `generative` | return/pass |
| `tests/doc_engine/test_spring_signal_scan_determinism_refs.py` | `tmp`, `result`, `entry`, `parse` | return/pass (+ pass `parse`) |
| `tests/doc_engine/test_gap_probe_ocs_real_world.py` | `report` | return/pass |

**Verdict:** **return→unpack→pass** for all four. Statement headroom remains under ≤20; intentional method merge (COH10) not required. Healthy pairs already use returns (climb tests). `[Evidenced]` pytest fixture cohesion (≥10k★ host) supports explicit dataflow over shared module globals for restore hooks.

**AST witness recipe (DoD):** run the inventory script shape used this spike; Accept when `broken==0`. Implement ships a pytest domain_ci_meta witness that encodes the same leak check (class-level).

---

## E-HOT-R2 — CQ hard-scope matrix `[Confirmed]`

Probes against tip `_hard_statement_scope` **before** HOT5:

| Key | Today hard? | After HOT5 (locked) |
| --- | --- | --- |
| `mod.py::f` (slash-free) | False | **True** (unit / scripts-only measure) |
| `scripts/ci/foo.py::f` | False | **False** (G6 debt measured, not hard) |
| `scripts/foo.py::g` | False | **False** |
| `src/doc_engine/x.py::h` | True | **True** |
| `tests/ci/t.py::i` | True | **True** |
| `tests/support/h.py::j` | True | **True** |

**DDIA:** hard-fail list = merge SoR; soft advisories = derived. Characterization tests lead production edit (TDD).

---

## E-HOT-R3 — Façade patch site `[Evidenced]` + `[Confirmed]`

- Call site: `certification_finish.write_certification_and_finish` → local name `build_and_write_certification` (same module globals).
- Façade `support._build_and_write_certification` is a re-export; patching it does **not** intercept the in-module call.
- **Patch target:** `doc_engine.pipeline.local_runner_phases.certification_finish.build_and_write_certification`.
- **Refuse:** teaching fold to accept bare `str` (dual API SoR). `[Evidenced]` pytest monkeypatch “patch where used” (pytest ≥14k★).

---

## E-HOT-R4 — Verify pack DoD `[Confirmed]`

Boolean pack before push:

1. Focused pytest: CQ ratchet, size helpers, cert finish, pipeline mock generative, scan contested, drift harness gate/semantic, metamorphic formatting, ddia prompt_10.
2. AST G2 `broken==0` (witness test or script).
3. `python3 scripts/ci/pre_pr.py --full` exit 0.
4. Touched-path compile/collect when 3.10 available; else note Unknown and rely on CI matrix.
5. Finding ledger + backlog P18.1 Archive.

**Net HOT7:** Defect **still present** (Confirmed 2026-08-09 focused run). Keep
known-moves ratchet; do **not** fold into invariant loop until residue empty.

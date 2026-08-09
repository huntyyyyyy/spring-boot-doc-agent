---
title: Tools wave 2 modularity — run_manifest + citation_coverage (2026)
status: E-MOD3 APPROVED (2026-08-09) · IMPLEMENTING
research date: 2026-08-09
claim tiers: Evidenced / Confirmed / Unknown
product: Python CLI doc-engine — Stage-0 / analytics tools BC
related:
  - docs/research/modularity/12-pipeline-stage0-modularity-ports-2026.md
  - docs/research/se-quality-synthesis-2026-08-08.md
  - docs/research/quality-backlog.md
do_not:
  - weaken fail_under 98.7, complexipy ≤5, LOC ≤225
  - introduce DI containers or utils/ grab-bags
  - pull scanning package or local_runner_phases/support into this tip
  - schedule Defer sensors (E-UX2 / E-QA3 / E-RUN*) as this tip
spec_gate: APPROVED E-MOD3 (2026-08-09) — MOD3-A–D (plan accept)
---

# Principal memo: tools wave 2 (`run_manifest`, `citation_coverage`)

**Question:** After E-MOD2, which grandfathered tools gods are the next single
modularity tip — and how do we split them without breaking climb monkeypatches
or live-gates `-m` entrypoints?

**Claim tiers:** `[Evidenced]` · `[Confirmed]` · `[Unknown]`.

---

## 0. One-page verdict

| Question | Answer |
| --- | --- |
| Next tip after E-MOD2? | **E-MOD3** — absolute LOC leaders `run_manifest` (~628) then `citation_coverage` (~521) `[Confirmed]` |
| E-SCAN1 / sensors? | **Next tip / Defer** — not this PR `[Confirmed]` backlog |
| Pattern? | Same as E-MOD2: concept modules ≤225 + thin façade + Protocol ports + façade DIP lookups `[Confirmed]` memo 12 MOD-S1 |
| Raise LOC hard cap? | **Refuse** |

---

## 1. Evidence inventory

| Claim | Tier | Source |
| --- | --- | --- |
| `run_manifest.py` LOC **628**; `citation_coverage.py` LOC **521** | Confirmed | `wc -l` + size baseline |
| Climb tests patch `rm.os` / `rm.subprocess` / `rm.dfs_walk` / `rm.compute_file_signature` / `rm.load_file_signatures` | Confirmed | `tests/doc_engine/test_coverage_climb_run_manifest_*.py` |
| Live gates invoke `python -m doc_engine.tools.citation_coverage` | Confirmed | `pipeline/live_gates.py` `MOD_CITATION` |
| No test monkeypatches `citation_coverage` module surface | Confirmed | citation unit tests call `cc.*` directly |
| E-MOD2 façade-late-import DIP pattern works | Confirmed | `capacity_preflight_compute` / `spring_drift_cli` |

---

## 2. Approve claims MOD3-A–D

| ID | Decision | Stance |
| --- | --- | --- |
| **MOD3-A** | `RunManifestStore` (load/write) + `RunManifestLifecycle` (init/start/end/finalize) **Protocols**; concept modules: constants / io / stages / finalize / summary / cli; creational factory only if construction branches earn it (default: plain functions + ports) | Adopt |
| **MOD3-B** | `CitationCoveragePort` (check_docs + total_findings) Protocol; split compute (claims / anchors) vs report/CLI I/O | Adopt |
| **MOD3-C** | Thin façades keep `from doc_engine.tools.run_manifest import …` and `-m citation_coverage` stable; helpers that climb/CLI patch resolve via **façade late import** (os, subprocess, dfs_walk, compute_file_signature, load_file_signatures) | Embody (DIP lesson) |
| **MOD3-D** | Out of scope: scanning package, `local_runner_phases/support.py`, sensor epics | Refuse this tip |

Human Approve = plan accept of MOD3-A–D (2026-08-09).

---

## 3. Target seam map

### `run_manifest` (`src/doc_engine/tools/`)

| Module | Responsibility |
| --- | --- |
| `run_manifest_constants.py` | Stage status sets, preflight→manifest map, tag key map |
| `run_manifest_io.py` | Atomic JSON write, git helpers, clocks / run_id |
| `run_manifest_stages.py` | `build_init_manifest`, `start_stage`, `end_stage` |
| `run_manifest_finalize.py` | Signatures, evidence tags, interview, preflight tie-in, `finalize_manifest` |
| `run_manifest_summary.py` | `format_summary` + line formatters |
| `run_manifest_cli.py` | Argparse + command handlers + `main` |
| `run_manifest_ports.py` | `RunManifestStore`, `RunManifestLifecycle` |
| `run_manifest.py` | Thin façade (re-export `os`/`subprocess`/`dfs_walk`/`compute_file_signature`) |

### `citation_coverage`

| Module | Responsibility |
| --- | --- |
| `citation_coverage_constants.py` | Windows, artifact/symbol patterns, structural regexes |
| `citation_coverage_claims.py` | Claim units, miscased tags, untagged claims |
| `citation_coverage_anchors.py` | Claim symbols, weak-anchor classification |
| `citation_coverage_report.py` | `check_docs`, `total_findings`, `format_report` |
| `citation_coverage_cli.py` | `main` |
| `citation_coverage_ports.py` | `CitationCoveragePort` |
| `citation_coverage.py` | Thin façade |

---

## 4. Epic tickets

| Epic | Status | Goal / exit |
| --- | --- | --- |
| **E-MOD3** | **Active** | Split both gods ≤225; ports; size `--update`; climb + citation + live-gates green |
| **E-SCAN1** | Suggested next | Scanning vertical modularity under existing `ScannerBackend` — **not this tip** |

---

## 5. Explicit refuse

Same as memo 12 §6, plus: do not start E-SCAN1 or Defer sensors in this tip.

---

## Invariants

fail_under **98.7** · complexipy **≤5** · LOC **≤225** · no `utils/` · policy **16-A** ·
SDD one tip · Spec → Implement → Verify → Archive.

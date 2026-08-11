---
title: Local domain pytest selection + fine ABI path shards (2026)
status: APPROVED — SPEC GATE E-SEL0 (2026-08-09)
date: '2026-08-09'
epic: E-SEL0
claim_tiers: Evidenced / Confirmed / Unknown
related:
- docs/design/local-domain-pytest-select-design-2026-08-09.md
- docs/design/test-suite-parallel-domains-design-2026-08-08.md
- docs/research/coverage-quality/08-rust-test-runners-bottlenecks.md
- docs/research/process/22-stack-rescope-10k-star-bar-2026.md
do_not:
- suite-wide xdist / -n on the 3.11 cov oracle cell
- pytest-testmon / RTS that skips merge oracle
- Adopt ★-wash selection plugins as SoT
last_reviewed: '2026-08-10'
---

# Process research: domain select + fine shards (E-SEL0)

## 1. Problem (Confirmed)

Local `pre_pr` pytest is ~57s of ~70s wall. ABI shards pass **parent dirs**
(`tests/doc_engine`, `tests/ci`) into `pytest $paths -m $marker`, so climb and
ci_meta jobs still **collect the fat mixed tree** then filter — modern sharding
done wrong.

## 2. Modern landscape (2026-08-09)

| Approach | Stars / surface | Stance here |
| --- | --- | --- |
| **CI marker/path shards before xdist** (pytest-xdist docs; industry 2026) | xdist ~1.9k; distribution modes Evidenced | **Embody** — already Spec **T-A** |
| **Fine path lists / matrix groups** (filesystem shard scripts; pytest-split class) | common CI pattern | **Adopt** — emit **file paths** when a collection dir mixes parallel markers |
| **pytest-xdist `-n` on oracle** | Evidenced primary | **Refuse** (constitution / T9 / E-RUN) |
| **pytest-testmon** (coverage DB RTS) | ~1003★ | **Defer/Refuse as SoT** — &lt;10k; never skip merge oracle (E-RUN4) |
| **NameRTS / path→test map behind pre_pr only** | research 08 D9/D18 | **Adopt** closed prefix→`domain_*` map; fail-closed → full `tests/` |

## 3. Verdict

**Embody T-A.** **Adopt** (1) fine ABI paths for mixed dirs, (2) deterministic
path→domain pytest argv on `pre_pr` **standard** (not oracle; not `--full`).
**Refuse** xdist-on-oracle and testmon-as-merge-SoT. **Adopt** local junit +
suite_timing summary so selection wins are measurable.

## 4. Spec

Design **SEL1–SEL10**; Implement **E-SEL1** so it **bites** (narrow pytest argv
+ regression tests; ABI matrix no longer lists sole `tests/doc_engine` for
climb when mixed).

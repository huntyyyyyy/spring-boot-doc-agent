---
id: architecture-decision-review
kind: playbook
completeness: operational
tags: [review, architecture, adr]
related: [trust-but-verify-and-auditability, maintainability-operability-evolvability, choosing-sor-vs-view, effective-remedies]
last_refined: 2026-08-09
path: playbooks/architecture-decision-review.md

---

# Playbook: architecture decision review

## Intent

Run a principal-level AD review using the north-star catalog plus prompt 10 evidence tiers — without re-reading the whole epub.

## Decision procedure

1. State the decision in one sentence and the blast radius.
2. INDEX → 1–2 concept/playbook pages; note each page’s `completeness`.
3. Classify artifacts as SoR vs view (`choosing-sor-vs-view`).
4. Demand witnesses (fixture, failing case, measurement) for load-bearing claims (prompt 10).
5. Record verdict with catalog `id` citations.

## Review procedure
- Fail if a dual writer, silent LWW, or vacuous gate ships without a deviation or SoR fix.

1. Skim diff for new writers, schemas, gates, baselines, docs paths.
2. Map each to a review trigger in README / INDEX.
3. For every “always”/“never” claim, require Tier A path or mark `unknown`.
4. Prefer closing a failure **class** (vacuous gate, LWW merge) over instance nits.
5. Output: confirmed / evidenced / contested / unknown — plus north-star ids.

## Do not

- Treat deepwiki.com or chat memory as Tier A.
- Fake `operational` authority from an `outline` chapter page.
- Expand scope into unrelated packaging mega-PRs.

## Worked example (this repo)

- Coverage SoR blindspot review → `claims-and-status-drift` + `coverage-gates` + `sor-vs-derived`.
- B2.5 cert review → `replication-lag-and-lww` + `choosing-sor-vs-view`.

## Repo path witness

- [Repo] `playbooks/architecture-decision-review.md`

## Effective remedies

- **Primary:** name one of `fitness-function` / `single-write-derive` / `characterization-net` / `adequacy-witness` / `sensor-ledger-spec` from [meta/effective-remedies.md](../meta/effective-remedies.md) by concern — DDIA id is vocabulary only (SOL1).
- **Accept:** ADR / review finding names **remedy mechanism id** + Accept = installed|Defer.
- **Fail if:** review cites only north-star concept ids with no remedy column.

## See also

- `docs/process/steering-prompts/10-review-persona-and-standards.md`

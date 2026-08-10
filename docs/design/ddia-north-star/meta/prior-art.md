# Prior art — Took / Declined / Why

Evidence log for external patterns considered while building this north-star and related gates. Not a scrape of deepwiki.com (Tier C). Prefer primary sources (papers, repo READMEs, RFCs).

**Last refined:** 2026-08-09.

## How to read

| Column | Meaning |
|--------|---------|
| **Took** | Adopted (or adapted) into this product / catalog |
| **Declined** | Explicitly not adopted |
| **Why** | One-sentence rationale tied to our SoR / constraints |

Add a row when a wave cites arXiv / GitHub / standards. Do not invent citations.

## Catalog and documentation structure

| Source | Took | Declined | Why |
|--------|------|----------|-----|
| DDIA 2e (Kleppmann & Riccomini) chapter atlases + concept vocabulary | Paraphrased domain/concept/relationship taxonomy; epub anchors as Tier A pointers | Vendoring epub or long verbatim excerpts | Copyright + catalog must remain decision SoR in-repo |
| Backstage software catalogs | Stable `id` + machine index (`catalog.json`) idea | Backstage as a runtime dependency | Too heavy; markdown+JSON is enough for principal SE lookup |
| ArchUnit / Archgate style rules-as-tests | Depth gate as fitness functions (`test_ddia_north_star_depth.py`) | Shipping ArchUnit/Java deps into this Python plugin | Wrong stack; pytest predicates already bite |

## Capacity / partitioning (Wave A / L2)

| Source | Took | Declined | Why |
|--------|------|----------|-----|
| DDIA ch07 partitioning / secondary indexes / rebalancing | Domain `07-partitioning-and-skew`; Stage-1 max vs Stage-4 upper_bound split | Treating fan-out warn-threshold raises as the fix | Band-aid on under-measurement |
| Partitioned join vs broadcast (this repo, commit abd3ade lesson) | Stage-1 slice stats; never re-measure removed broadcast | Reintroducing full references broadcast | Confirmed ~21× overstatement |

## Derived data processing (Wave B)

| Source | Took | Declined | Why |
|--------|------|----------|-----|
| DDIA ch10–12 batch/stream / serving derived data | Domain `09`; `rel-batch-feeds-serving`; stage+load | Live SoR writes from batch “for convenience” | Dual-writer class (`dev-certification-derived-view`) |
| Id-stable path moves | Relocated `batch-vs-stream-derived-state` under domain 09 | Renaming the catalog id | Ids are forever |

## Integrity / coverage (standing)

| Source | Took | Declined | Why |
|--------|------|----------|-----|
| Separate precision (FP ratchet) vs recall baselines | `dev-fp-ratchet-separate-from-recall`; hermetic negatives | Inventing client-named recall corpora | No licensed corpus; would fake confidence |

## Concern → remedy mechanisms (Wave SOL / 2026-08-09)

| Source | Took | Declined | Why |
|--------|------|----------|-----|
| Ford evolutionary architecture / fitness functions; ArchUnit-style rules-as-tests | `fitness-function` mechanism; G2 AST witness; tach cycles; depth gate | Shipping ArchUnit/Java or dual architecture linters | Wrong stack; pytest fitness already bites |
| Outbox / CDC single-write + derive; arXiv 2608.00501 | `single-write-derive`; policy **16-A** oracle vs climb | Treating every log as a message bus | Pattern transfer to artifacts/APIs only |
| Feathers characterization tests; 2026 agent-refactor practice | `characterization-net` before E-COH reshape | “Fix while extracting” without a net | Agents amplify blast radius |
| Mutmut / metamorphic adequacy / E-QA SMS·MC | `adequacy-witness` as gate witness class | Mutation or Cover% as fail_under substitute | Cover% necessary≠sufficient |
| E-STK0 / react-doctor stalker pattern | `sensor-ledger-spec` | Watch agent as silent tip fixer | Spec gate stays human |

Research SoR: `docs/research/process/23-concern-to-solution-remedies-2026.md`. Catalog companion: [effective-remedies.md](effective-remedies.md).

## Intentionally not researched yet

Promote domain `06` / lite concurrency-consensus concepts when concurrent writers or consensus actually bite. Additional arXiv rows only when those waves need them.

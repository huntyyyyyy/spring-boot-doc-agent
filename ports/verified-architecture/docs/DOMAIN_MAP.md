# Domain map — forced entry

Open this before deep work; then only the paths for the task. Prefer
`00/`–`12/` ([PRECODE_MAP.md](../PRECODE_MAP.md)). Flat `docs/` below = legacy
except Architecture Decision Records / C4 / standards.

## Standards

| Topic | Path |
| --- | --- |
| No-code gate | `docs/standards/no-code-gate.md` |
| ISO 29148-shaped requirements engineering | `docs/standards/iso-29148-re.md` |
| Architecture Tradeoff Analysis Method Quality Attribute Scenario | `docs/standards/quality-attribute-scenarios.md` |
| Constraints vs requirements | `docs/standards/constraints-vs-requirements.md` |
| Architecture Decision Record (Nygard) | `docs/standards/adr-standard.md` |
| C4 | `docs/standards/c4-standard.md` |
| Claim tiers | `docs/standards/research-method.md` |

## Requirements System of Record

| Artifact | Path |
| --- | --- |
| Stakeholder Requirements Specification | `03-requirements/strs/strs-wave1.md` |
| Software Requirements Specification | `03-requirements/srs/srs-wave1.md` |
| Quality Attribute Scenario | `03-requirements/qas/` |
| Requirements Traceability Matrix | `03-requirements/rtm/rtm-wave1.md` |
| Constraints | `04-constraints/technical/constraints-wave1.md` |
| Legacy pointers | `docs/requirements/`, `docs/constraints/` |

## Architecture

| Artifact | Path | Note |
| --- | --- | --- |
| C4 Context / Container / Component | `docs/c4/01…03-*.md` | Code level: `04-code.md` |
| Architecture Decision Records | `docs/adr/README.md` | Not under `07/` |
| Confidence sketch (not full C4) | `07-system-design/c4/C4-BRIEF-CONFIDENCE.md` | — |

## Research (evidence — one pack)

| Domain | Path |
| --- | --- |
| Catalog | `research/INDEX.md` |
| Layers of Truth | `research/layers-of-truth/` |
| Adversarial / overturn | `research/adversarial/` |
| Polyglot | `research/polyglot/` |
| Architecture Tradeoff Analysis Method / formal | `research/atam-formal/` |
| Cursor rule / DevEx | `research/mdc-devex/` |

## Language nests (options, not Approved Design)

| Nest | Enter when | Lock |
| --- | --- | --- |
| `nests/01-engine-rust` | Engine / resolve / receipts | **Spec corpus Model Context Protocol host** |
| `nests/02-registry-sqlite` | Registry schema | — |
| `nests/03-locks-ruby` | Packwerk-shaped locks | Not tip kernel |
| `nests/04-chassis-go` | Watch / reindex daemon | Not tip kernel |
| `nests/05-graph-clojure` | Datascript graph brain | Not merge authority |
| `nests/06-sandbox-wasm` | LockCheck guest | **Could / Wave-3** — not Spec host |
| `nests/07-ide-typescript` | IDE / presentation Model Context Protocol | **Not** Spec corpus server default |
| `nests/08-aci-python-peer` | — | **REFUSED** (tombstone only) |
| `nests/09-native-c-zig` | Earned native shims | — |

# Domain map — forced entry

**Rule for agents:** open this file before deep work. Then open only the
paths listed for the task. Nest MDC files restate a narrower map.

**Preferred tree (BFS pre-code):** [PRECODE_MAP.md](../PRECODE_MAP.md) and
folders `00-governance/` … `12-delivery/`. Flat `docs/` below is legacy until
promoted.

## Working draft + standards

| Topic | Path |
| --- | --- |
| No-code gate | `docs/standards/no-code-gate.md` |
| ISO 29148-shaped RE | `docs/standards/iso-29148-re.md` |
| Architecture Tradeoff Analysis Method Quality Attribute Scenario | `docs/standards/quality-attribute-scenarios.md` |
| Constraints vs REQs | `docs/standards/constraints-vs-requirements.md` |
| Architecture Decision Record (Nygard) | `docs/standards/adr-standard.md` |
| C4 | `docs/standards/c4-standard.md` |
| Claim tiers | `docs/standards/research-method.md` |

## Requirements System of Record

| Artifact | Path |
| --- | --- |
| Stakeholder Requirements Specification | `docs/requirements/strs.md` |
| Software Requirements Specification | `docs/requirements/srs.md` |
| Quality Attribute Scenario | `docs/requirements/qas.md` |
| Requirements Traceability Matrix | `docs/requirements/rtm.md` |
| Constraints | `docs/constraints/constraints.md` |

## Architecture

| Artifact | Path |
| --- | --- |
| C4 Context | `docs/c4/01-context.md` |
| C4 Containers | `docs/c4/02-containers.md` |
| C4 Components (engine) | `docs/c4/03-components.md` |
| Architecture Decision Records | `docs/adr/README.md` |

## Research corpus (Retrieval-Augmented Generation — evidence, not fluff)

| Domain | Path |
| --- | --- |
| Catalog (ingest map) | `research/INDEX.md` |
| Layers of Truth / vision | `research/layers-of-truth/` |
| Adversarial + RE critique | `research/adversarial/` |
| Polyglot mental models + portfolio | `research/polyglot/` |
| Architecture Tradeoff Analysis Method / formal boundaries | `research/atam-formal/` |
| MDC / DevEx / context | `research/mdc-devex/` |
| Provenance | `research/PROVENANCE.md` |

## Nested bounded contexts (progressive context)

| Nest | Language | Enter when… |
| --- | --- | --- |
| `nests/01-engine-rust` | Rust | Engine / resolve / receipts |
| `nests/02-registry-sqlite` | SQLite | Registry schema |
| `nests/03-locks-ruby` | Ruby | Packwerk-shaped locks |
| `nests/04-chassis-go` | Go | Watch / reindex daemon |
| `nests/05-graph-clojure` | Clojure | Datascript graph brain |
| `nests/06-sandbox-wasm` | WebAssembly | Capability LockCheck guest |
| `nests/07-ide-typescript` | TypeScript | IDE / Model Context Protocol UI |
| `nests/08-aci-python-peer` | Python | Optional ACI peer (not majority) |
| `nests/09-native-c-zig` | C / Zig | Earned native shims |

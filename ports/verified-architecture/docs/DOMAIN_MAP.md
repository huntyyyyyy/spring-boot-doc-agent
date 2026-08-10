# Domain map — forced entry

**Rule for agents:** open this file before deep work. Then open only the
paths listed for the task. Nest MDC files restate a narrower map.

## Working draft + standards

| Topic | Path |
| --- | --- |
| No-code gate | `docs/standards/no-code-gate.md` |
| ISO 29148-shaped RE | `docs/standards/iso-29148-re.md` |
| ATAM QAS | `docs/standards/quality-attribute-scenarios.md` |
| Constraints vs REQs | `docs/standards/constraints-vs-requirements.md` |
| ADR (Nygard) | `docs/standards/adr-standard.md` |
| C4 | `docs/standards/c4-standard.md` |
| Claim tiers | `docs/standards/research-method.md` |

## Requirements SoR

| Artifact | Path |
| --- | --- |
| StRS | `docs/requirements/strs.md` |
| SRS | `docs/requirements/srs.md` |
| QAS | `docs/requirements/qas.md` |
| RTM | `docs/requirements/rtm.md` |
| Constraints | `docs/constraints/constraints.md` |

## Architecture

| Artifact | Path |
| --- | --- |
| C4 Context | `docs/c4/01-context.md` |
| C4 Containers | `docs/c4/02-containers.md` |
| C4 Components (engine) | `docs/c4/03-components.md` |
| ADRs | `docs/adr/README.md` |

## Research corpus (RAG — evidence, not fluff)

| Domain | Path |
| --- | --- |
| Catalog (ingest map) | `research/INDEX.md` |
| Layers of Truth / vision | `research/layers-of-truth/` |
| Adversarial + RE critique | `research/adversarial/` |
| Polyglot mental models + portfolio | `research/polyglot/` |
| ATAM / formal boundaries | `research/atam-formal/` |
| MDC / DevEx / context | `research/mdc-devex/` |
| Provenance | `research/PROVENANCE.md` |

## Nested BCs (progressive context)

| Nest | Language | Enter when… |
| --- | --- | --- |
| `nests/01-engine-rust` | Rust | Engine / resolve / receipts |
| `nests/02-registry-sqlite` | SQLite | Registry schema |
| `nests/03-locks-ruby` | Ruby | Packwerk-shaped locks |
| `nests/04-chassis-go` | Go | Watch / reindex daemon |
| `nests/05-graph-clojure` | Clojure | Datascript graph brain |
| `nests/06-sandbox-wasm` | WASM | Capability LockCheck guest |
| `nests/07-ide-typescript` | TypeScript | IDE / MCP UI |
| `nests/08-aci-python-peer` | Python | Optional ACI peer (not majority) |
| `nests/09-native-c-zig` | C / Zig | Earned native shims |

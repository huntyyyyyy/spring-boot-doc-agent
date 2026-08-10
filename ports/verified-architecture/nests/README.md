# Nested repositories (progressive context)

Each nest is a **future first-class BC** (and later may become its own git
subtree or repo). Until the no-code gate clears, nests hold:

- `README.md` — ownership, ADRs, research pointers  
- `.cursor/rules/nest.mdc` — agent look-first for *this* nest only  

When you work in a nest, Cursor/agents should prefer that nest’s MDC so they
load **shared SoR + this BC’s research**, not the entire monorepo dump.

| Nest | BC | Primary ADRs | Research entry |
| --- | --- | --- | --- |
| 01-engine-rust | Engine | 0007, 0004, 0002 | `research/layers-of-truth/`, `research/polyglot/` |
| 02-registry-sqlite | Registry | 0002 | `research/polyglot/` (SQLite section) |
| 03-locks-ruby | Lock DX | 0003 | Packwerk history in `research/polyglot/` |
| 04-chassis-go | Daemon | 0009 | Cobra chassis in `research/polyglot/` |
| 05-graph-clojure | Graph brain | 0005 | Datascript/bb in `research/polyglot/` |
| 06-sandbox-wasm | WASM guest | 0004 | `research/atam-formal/` formal boundaries |
| 07-ide-typescript | IDE/MCP | 0010 | C4 containers |
| 08-aci-python-peer | Optional ACI | 0001, 0006 | Peer only — not majority engine |
| 09-native-c-zig | C/Zig shims | 0001 | Earned Spikes only |

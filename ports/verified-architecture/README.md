# Verified Architecture Engine — planning repository

**Working draft.** Requirements · constraints · research · C4 · ADRs.  
**No product code** until the CONTRIBUTING gate is green.

Follows industry planning practice shaped by **ISO/IEC/IEEE 29148** (RE),
**SEI ATAM** quality-attribute scenarios, **Nygard ADRs**, and **C4** models.
Claim tiers: Evidenced / Confirmed / Unknown. This is intentionally a
**living draft** — statuses are Proposed/Draft until stakeholder Accept.

## How this repo is meant to be used (nested context)

```text
.cursor/rules/          ← repo-wide MDC (constitution, look-first, draft/ISO)
docs/                   ← SoR: requirements, constraints, standards, C4, ADRs
research/               ← full research corpus (keep — this is the value)
nests/<NN>-<bc>/        ← N nested “next repos”: each has README + .cursor/rules
                          so agents load only that BC’s context when working there
```

1. Open [`docs/DOMAIN_MAP.md`](docs/DOMAIN_MAP.md) first (forced entry).  
2. Load research under `research/` as needed — **do not discard**; it is the
   evidence base.  
3. When implementing a BC later, work inside `nests/<bc>/` so nest MDC scopes
   context to that language/BC while still pointing at shared research/ADRs.

## Polyglot identity

Rust · WASM · SQLite · Go · Ruby · Clojure · TypeScript · Python (peer) · C · Zig (earned).  
Not a Python-majority doc-engine port. See ADR-0001 + `research/polyglot/`.

## Start reading

| Priority | Path |
| --- | --- |
| Map | [`docs/DOMAIN_MAP.md`](docs/DOMAIN_MAP.md) |
| Standards | [`docs/standards/`](docs/standards/) |
| Requirements | [`docs/requirements/`](docs/requirements/) |
| Constraints | [`docs/constraints/constraints.md`](docs/constraints/constraints.md) |
| C4 | [`docs/c4/`](docs/c4/) |
| ADRs | [`docs/adr/`](docs/adr/) |
| Research | [`research/README.md`](research/README.md) |
| Nests | [`nests/README.md`](nests/README.md) |

Export to a standalone GitHub remote: [`EXPORT.md`](EXPORT.md).

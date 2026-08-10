# Contributing — planning gates before code

## Hard gate

**No product implementation** (Rust crates, Go daemon, Ruby gems, Clojure
services, WASM guests, TS extensions, Python packages, C/Zig shims) until:

1. **StRS / SRS / RTM** Approved (or explicitly wave-scoped) under `docs/requirements/`
2. **Constraints** ledger current under `docs/constraints/`
3. Every Must **NFR** is a completed **ATAM QAS** (`docs/requirements/qas.md`)
4. **C4** Context + Container (+ Component for touched BCs) reviewed (`docs/c4/`)
5. Relevant **ADRs** Accepted (`docs/adr/`) — diagrams cite ADR IDs
6. Utility / **tradeoff** table updated for chosen tactics

Until then, PRs may only change `docs/**`, this file, README, LICENSE, and
planning CI that **lints docs** (no compile of product code).

## Standards

See [`docs/standards/`](docs/standards/).

## After gates

Implementation follows polyglot BCs in
[`docs/architecture/polyglot-portfolio.md`](docs/architecture/polyglot-portfolio.md)
with keep/drop Spikes and a **single** deterministic gate writer (language chosen
by ADR — not assumed Python).

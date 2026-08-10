# AGENTS.md

Thin Cursor Cloud ingest layer. Repo working conventions SoT: `CLAUDE.md`.
Agent **path/task scoping** SoT: Project Rules under `.cursor/rules/` (MDC
`alwaysApply` / `globs` / agent-requested / manual). Do **not** add nested
`AGENTS.md` files for path scoping beside those globs.

## Orientation (start here)

| Pointer | Why |
| --- | --- |
| [`DOMAIN_MAP.md`](DOMAIN_MAP.md) | Product BCs, truth classes, refuse list |
| [`docs/research/quality-backlog.md`](docs/research/quality-backlog.md) | **One** Active tip |
| [`.cursor/rules/`](.cursor/rules/) | Activation algebra (constitution + lenses) |
| [`.cursor/skills/principal-se-research-epic/SKILL.md`](.cursor/skills/principal-se-research-epic/SKILL.md) | Design-shaped: digests + Bloom Create + DeepWiki |
| [`.cursor/skills/paper-digest/SKILL.md`](.cursor/skills/paper-digest/SKILL.md) | arXiv digests: type keys, sections, refs, GitHub anti-bogus |
| [`docs/research/method/paper-digest-framework.md`](docs/research/method/paper-digest-framework.md) | Paper-digest method Source of Truth |
| [`.cursor/skills/cross-domain-isomorphism/SKILL.md`](.cursor/skills/cross-domain-isomorphism/SKILL.md) | Structure-Adopt vs Substrate-Refuse |

Stay on the Active tip branch/PR from the backlog. Do not invent a parallel tip.

## Cloud environment (minimal)

- Python 3.10+ CLI/SDK (`doc-engine`); no app server/DB. Optional tools may egress.
- Activate `.venv/` before lint/test/run (`README.md`, `.github/workflows/ci.yml`).
- Pin-check: `ast-grep` / `semgrep` must match `requirements.txt` on `PATH`.
- Before push (non-docs): `python3 scripts/ci/pre_pr.py --auto`. Outage:
  `--actions-outage`. Details: rule `ci-local-gates` + `scripts/README.md`.
- Touches to `scripts/` / `agents/` / `skills/`: `python3 scripts/ci/check_repo_claims.py`.
- Hard denies: project [`.cursor/hooks.json`](.cursor/hooks.json) (not user-global).

## Gotchas (one-liners)

- `doc-engine certification verify` rejects `none`/`mock` generative executor unless `--allow-mock`.
- Main `ci.yml` smoke only checks `certification.json` **exists**; verify jobs live in `doc-engine.yml`.
- Pipe to `tail`/`head` can mask non-zero exits — redirect to a file; check `$RC` (`docs/process/tool-quirks.md`).

# Local grading pack (Windows + OCS)

Human checklist only. **Do not use IntelliJ’s Markdown play button** on this
file — it runs cmd/PowerShell, treats `##` as junk, and is not Git Bash.

## How to run (IntelliJ / Windows)

1. Open a **Git Bash** terminal, *or* right-click / Run:

   - `scripts/ci/run_local_grading_pack.cmd` (finds Git Bash for you)
   - `scripts/ci/run_local_grading_pack.sh` (Linux / already-in-bash)

2. From the **doc-engine** repo root (examples):

```text
scripts\ci\run_local_grading_pack.cmd doctor
scripts\ci\run_local_grading_pack.cmd list
scripts\ci\run_local_grading_pack.cmd priority1
scripts\ci\run_local_grading_pack.cmd p1 p2
scripts\ci\run_local_grading_pack.cmd p3
```

3. Logs land in `local-runs/logs/<id>.log` with an `EXIT:` line. Send those.

IntelliJ tip: Run Configuration → Batch / Shell Script → target the `.cmd`
file; Working directory = doc-engine root. Optional env: `GIT_BASH` =
`C:\Program Files\Git\bin\bash.exe`.

## Venv hygiene (new terminal)

```text
cd /c/path/to/spring-boot-doc-agent
source .venv/Scripts/activate
which python
which ast-grep
ast-grep --version
```

First `which` hits must be under `.venv/Scripts`. Skip `pip install` if that
already works (corp TLS often breaks PyPI). JDK `cacerts` does **not** fix pip
— see `docs/process/tool-quirks.md` (2026-08-10).

## Prereqs (only when tools missing)

Prefer the runner’s `doctor` first. If you must install:

```text
export PIP_CERT="/path/to/corp-root.pem"   # NOT JDK cacerts
pip install -r requirements.txt -r requirements-dev.txt && pip install -e .
npm ci   # only needed before H7 quality-gates
```

OCS pointer (gitignored; no quotes inside the file):

```text
echo C:/dossier/.../ocs-api-service > local-runs/real-repo.path
```

Legend: **SoR** = merge/CI source of record · **Campaign** = OCS opt-in ·
**Sensor** = informative only.

---

## Priority 1 — OCS campaign (run `priority1` then `p3`)

| ID | Runner arg | Proves | Capture |
|----|------------|--------|---------|
| P1 | `p1` | Checkout + Artifactory preflight | `p1-plant-profile.log` |
| P2 | `p2` | Offline floors. Expect **path_prefix ≈ 35**, marker maybe 8 | `p2-remeasure.log` |
| P3 | `p3` | Full OCS CodeQL plant + asserts | `p3-run-plant-ocs.log` + `harness/out/*.csv` |
| P4 | `p4` | ApiSurface ↔ OpenAPI join (after P3) | `p4-join-openapi.log` |

P3 needs VPN + `artifactory_user` / `artifactory_password`, CodeQL, Java 17,
Gradle. Very slow.

---

## Priority 2 — hermetic merge bar

| ID | Runner arg | Proves | Capture |
|----|------------|--------|---------|
| H1 | `h1` | `pre_pr --fast` | `h1-pre-pr-fast.log` + receipt |
| H2 | `h2` | `pre_pr --auto` | `h2-pre-pr-auto.log` |
| H3 | `h3` | Vacuity gate | `h3-vacuity.log` |
| H4 | `h4` | CodeQL rule_coverage (fixture) | `h4-rule-coverage.log` |
| H5 | `h5` | Semgrep rule coverage | `h5-semgrep-coverage.log` |
| H6 | `h6` | Cover% oracle 98.7 | `h6-coverage-measure.log` + `coverage.xml` |
| H7 | `h7` | quality-gates vs `origin/main` | `h7-quality-gates.log` |
| H8 | `h8` | Fixture plant | `h8-run-plant-fixture.log` |
| H9 | `h9` | CodeQL pack invariants | `h9-invariants.log` |

Bundle `hermetic-lite` = `h1 h9 h3 h4`. Fetch `origin/main` before `h7`.

---

## Priority 3 — OCS offline (no Artifactory)

| ID | Runner arg | Proves | Capture |
|----|------------|--------|---------|
| O1 | `o1` | Regen real-repo Stage-0 artifacts | `o1-regen.log` |
| O4 | `o4` | Capacity preflight | `o4-capacity.log` |

More Path A / adversarial steps stay manual; extend the runner when you need
them logged the same way.

---

## Adversarial extras

| ID | Runner arg | Notes |
|----|------------|--------|
| path_prefix dump | `adv-path-prefix` | Class-level only; ~35 not 45 |
| Messaging=0 | (manual) | No kafka/rabbit/sqs/pulsar/jms in OCS Gradle; paste “none” or lines |
| QL ↔ ast-grep | (after p3) | Compare CSV `rule_id` counts to `p2` floors |

---

## What to send for grading

1. `local-runs/logs/*.log` (with `EXIT:`), plus `coverage.xml` / receipt when relevant.
2. Never send Artifactory passwords, PEM, or OCS source trees.
3. Failures are as useful as greens.

## Windows gotchas

- Markdown play ≠ Bash. Use the `.cmd` launcher.
- `WinError 2` on `ast-grep` → activate venv / pull tip sibling resolve.
- Plant scripts need Git Bash + `sha256sum`.
- Prefer `C:/...` in `real-repo.path`.

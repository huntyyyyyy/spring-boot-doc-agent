# Local grading pack (Windows + OCS)

Operator checklist for producing logs so a remote session can grade execution.
Run from the **doc-engine** clone (not the OCS tree). Capture every command with:

```bash
CMD > "local-runs/logs/<id>.log" 2>&1; echo EXIT:$? | tee -a "local-runs/logs/<id>.log"
```

Use Git Bash. Activate `.venv` first (`source .venv/Scripts/activate`) so
`python`/`ast-grep`/`semgrep` match pins. Never pipe through `tail`/`head` as
the only consumer — that masks non-zero exits.

Prereqs once:

```bash
mkdir -p local-runs/logs
pip install -r requirements.txt -r requirements-dev.txt && pip install -e .
npm ci   # jscpd for quality-gates
# OCS pointer (gitignored; forward slashes OK):
#   echo C:/dossier/.../ocs-api-service > local-runs/real-repo.path
```

Legend: **SoR** = merge/CI source of record · **Campaign** = OCS opt-in ·
**Sensor** = informative only.

---

## Priority 1 — already partly green; finish these first

| ID | Command | Proves | SoR | Capture |
|----|---------|--------|-----|---------|
| P1 | `python spring-signals/harness/plant_profile.py --plant ocs --json` | Checkout + Artifactory preflight | Campaign | `logs/p1-plant-profile.log` |
| P2 | `python scripts/ci/remeasure_ocs_floors.py --checkout "$(cat local-runs/real-repo.path)"` | Offline floors dry-run. Expect **path_prefix ≈ 35** (class-level), not 45. Marker may be 8. | Campaign | `logs/p2-remeasure.json` (stdout is JSON) |
| P3 | `./spring-signals/harness/run-plant.sh ocs` | Full OCS CodeQL DB + wave-1 CSVs + asserts vs `ocs-api-service.json` | Campaign | `logs/p3-run-plant-ocs.log` + copy `spring-signals/harness/out/*.csv` listing / assertion block |
| P4 | `python spring-signals/harness/join_openapi.py --api-surface spring-signals/harness/out/ApiSurface.csv --openapi "$(cat local-runs/real-repo.path)/src/docs/api/OASv3/ocs-api-service.yaml"` | ApiSurface ↔ OpenAPI join (path may differ — confirm under OCS `**/OASv3/*.yaml`) | Campaign | `logs/p4-join-openapi.log` |

P3 needs VPN + `artifactory_user` / `artifactory_password`, CodeQL on PATH,
Java 17, Gradle. Very slow. If create-db fails, stop and send that log before
re-running queries.

---

## Priority 2 — hermetic merge bar (no OCS)

| ID | Command | Proves | SoR | Capture |
|----|---------|--------|-----|---------|
| H1 | `python scripts/ci/pre_pr.py --fast` | Tier-0: YAML, pins, ruff, claims, denylist | Local / CI-adjacent | `logs/h1-pre-pr-fast.log` + `.git/pre-pr-receipt.json` |
| H2 | `python scripts/ci/pre_pr.py --auto` | Path-routed standard hard suites (quality, markers, poke, vacuity, rule coverage, pytest/oracle slice) | Local choke point | `logs/h2-pre-pr-auto.log` + receipt + `.git/pre-pr-pytest.junit.xml` if present |
| H3 | `python scripts/ci/vacuous_test_gate.py` | Vacuous-test hard gate | Local / pre_pr | `logs/h3-vacuity.log` |
| H4 | `python scripts/coverage/rule_coverage.py` | Every CodeQL pack id fires on fixture corpus | **CI SoR** | `logs/h4-rule-coverage.log` |
| H5 | `python scripts/coverage/semgrep_rule_coverage.py` | Semgrep non-vacuity + FP ratchet | **CI SoR** | `logs/h5-semgrep-coverage.log` |
| H6 | `doc-engine coverage-measure` | Whole-repo Cover% (fail_under 98.7) | **CI Cover% SoR** (prefer 3.11) | `logs/h6-coverage-measure.log` + `coverage.xml` |
| H7 | `doc-engine quality-gates --compare-ref origin/main` | diff-cover / jscpd / complexipy / size / tach | **CI quality SoR** | `logs/h7-quality-gates.log` |
| H8 | `./spring-signals/harness/run-plant.sh fixture` | Credential-free fixture CodeQL plant + asserts | **CI CodeQL SoR** | `logs/h8-run-plant-fixture.log` + `harness/out-fixture/*.csv` if present |
| H9 | `python spring-signals/harness/check-invariants.py` | Pack layering / or-or lint (no CodeQL CLI) | CI invariants | `logs/h9-invariants.log` |

Pull `origin/main` (or fetch) before H7 so `--compare-ref` resolves.

---

## Priority 3 — OCS offline product lane (no Artifactory)

| ID | Command | Proves | SoR | Capture |
|----|---------|--------|-----|---------|
| O1 | `DOC_ENGINE_REAL_REPO="$(cat local-runs/real-repo.path)" python scripts/ci/regen_real_repo_artifacts.py` | Regen Stage-0 real-repo artifacts | Campaign / merge-readiness | `logs/o1-regen.log` + `local-runs/real-repo-latest/*` |
| O2 | `DOC_ENGINE_REAL_REPO="$(cat local-runs/real-repo.path)" DOC_ENGINE_REAL_ARTIFACTS_DIR=local-runs/real-repo-latest pytest tests/doc_engine/test_real_fixture_adversarial.py tests/doc_engine/test_etl_adversarial.py -v --tb=short` | Adversarial gap/ETL on real artifacts | Local | `logs/o2-adversarial.log` |
| O3 | `doc-engine pipeline run "$(cat local-runs/real-repo.path)" --compliance-profile deterministic_only --skip-drift --out-dir local-runs/ocs-det-$(date +%Y%m%d)` | Path A Stage-0 on real OCS | Campaign | `logs/o3-pipeline-det.log` + that out-dir’s `spring_signals.json` + `certification.json` |
| O4 | `python -m doc_engine.tools.capacity_preflight "$(cat local-runs/real-repo.path)"` | Scale / fan-out estimate | Sensor | `logs/o4-capacity.log` |
| O5 | `python scripts/coverage/rule_coverage.py "$(cat local-runs/real-repo.path)"` | Real-corpus recall backtest (sensor) | Sensor | `logs/o5-rule-coverage-ocs.log` |

---

## Priority 4 — deep / optional

| ID | Command | Proves | SoR | Capture |
|----|---------|--------|-----|---------|
| D1 | `python scripts/ci/pre_pr.py --full` | Standard + Stage-0 portable + mutate / mutation_driver | Local depth | `logs/d1-pre-pr-full.log` + receipt |
| D2 | `python scripts/ci/pre_pr.py --actions-outage` | Local CI parity incl. CodeQL compile/runtime + cert verify | Interim Actions substitute | `logs/d2-actions-outage.log` + receipt (`attestation: actions_outage`) |
| D3 | Fixture scan_only + verify (see `README` / `doc-engine.yml`): `doc-engine pipeline run scripts/fixtures/spring_signals --compliance-profile scan_only --out-dir local-runs/scan-only --skip-drift --signals-file scripts/fixtures/spring_signals_fixture_expected.json` then `doc-engine certification verify --allow-mock local-runs/scan-only/certification.json` | Fixture certification path | CI doc-engine | both logs + cert |
| D4 | CodeQL pack: from `spring-signals/codeql/` — `codeql pack install --no-strict-mode .` then `codeql query compile --check-only .` then `codeql test run .` | Pack compile + QL unit tests | CI when fingerprint changes | `logs/d4-codeql-pack.log` |
| D5 | `doc-engine coverage-measure --mode climb --scope <pkg>` | Climb sensor only | **Never** merge Cover% | `coverage.climb.xml` + log |
| D6 | Messaging spot-check on OCS (manual): search build files for kafka/rabbit/sqs/pulsar/jms; expect **zero** deps while `Messaging` asserted empty | Supports campaign Messaging=0 | Campaign evidence | paste build snippet + note |

---

## Adversarial gaps — extra evidence (short)

These close open grading questions; run after P2/P3 when possible.

1. **path_prefix predicate (CodeQL SoR)** — plant floor is **35** class-level.
   Tip rules exclude method-level `@RequestMapping`. After `git pull`, remeasure
   should report ~35, not 45. If you still see 45, you are on the old rule YAML.

   ```bash
   ast-grep scan -r spring-signals/harness/astgrep_ocs_floors.yml \
     --filter api_surface__path_prefix \
     "$(cat local-runs/real-repo.path)/src/main/java" \
     > local-runs/logs/adv-path-prefix.txt 2>&1
   ```

2. **repository_marker 8** — same with `--filter persistence__repository_marker`.
   Compare to `Persistence.csv` `persistence__repository_marker` row count after P3.

3. **QL ↔ ast-grep join** — after P3, compare CSV rule_id counts to P2 floors
   (controller / endpoint / path_prefix / marker); paste both number sets.

4. **Messaging=0** — confirm no kafka/rabbit/sqs/pulsar/jms in OCS Gradle files;
   plant `Messaging` asserted empty. Paste matching dependency lines or “none”.

---

## How to send logs for grading

1. Zip or paste: `local-runs/logs/*.log`, `coverage.xml` (if H6), `.git/pre-pr-receipt.json`, and for P3 the assertion summary + `wc -l` / head of each `out/*.csv`.
2. Do **not** send: Artifactory passwords, PEM/corp CA, OCS source trees, or paths that embed denylisted client tokens beyond what plant_profile already prints.
3. One batch per priority is enough (P → H → O → D). Failures are as useful as greens — include `EXIT:` lines.

## Windows gotchas (grading false fails)

- `WinError 2` on `ast-grep` → activate venv or pull tip that resolves sibling `ast-grep.exe`.
- `run-plant.sh` / `create-db.sh` need Git Bash + `sha256sum`; CodeQL Windows tracer often needs a `.bat` build command (see `docs/process/tool-quirks.md`).
- `setup_codeql.sh` defaults to linux64 — on Windows set matching `CODEQL_BUNDLE_URL` / `CODEQL_SHA256`.
- Prefer `C:/...` in `real-repo.path` (no quotes inside the file).

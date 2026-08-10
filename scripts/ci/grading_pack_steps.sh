#!/usr/bin/env bash
# Step implementations for run_local_grading_pack.sh (sourced, not executed).
# shellcheck shell=bash

cmd_doctor() {
  _activate_venv
  echo "ROOT=$ROOT"
  echo "python=$(command -v python || true)"
  echo "python3=$(command -v python3 || true)"
  echo "ast-grep=$(command -v ast-grep || true)"
  ast-grep --version 2>&1 || true
  python -c "import sys; print('prefix=', sys.prefix)" 2>&1 || true
  if path="$(_ocs_path)"; then
    echo "ocs=$path"
    [[ -d "$path" ]] && echo "ocs_dir=ok" || echo "ocs_dir=MISSING"
  else
    echo "ocs=UNSET (local-runs/real-repo.path or DOC_ENGINE_REAL_REPO)"
  fi
  echo "artifactory_user=${artifactory_user:+set}"
  echo "artifactory_password=${artifactory_password:+set}"
}

cmd_p1() {
  _activate_venv
  _run_logged p1-plant-profile \
    python spring-signals/harness/plant_profile.py --plant ocs --json
}

cmd_p2() {
  _activate_venv
  local ocs
  ocs="$(_ocs_path)" || {
    echo "error: set DOC_ENGINE_REAL_REPO or local-runs/real-repo.path" >&2
    return 2
  }
  _run_logged p2-remeasure \
    python scripts/ci/remeasure_ocs_floors.py --checkout "$ocs"
}

cmd_p3() {
  _activate_venv
  _run_logged p3-run-plant-ocs \
    bash spring-signals/harness/run-plant.sh ocs
}

cmd_p4() {
  _activate_venv
  local ocs yaml
  ocs="$(_ocs_path)" || return 2
  yaml="$(find "$ocs" -path '*/OASv3/*.yaml' 2>/dev/null | head -n 1 || true)"
  if [[ -z "$yaml" ]]; then
    echo "error: no OASv3 yaml under $ocs - set OPENAPI_YAML=" >&2
    return 2
  fi
  yaml="${OPENAPI_YAML:-$yaml}"
  _run_logged p4-join-openapi \
    python spring-signals/harness/join_openapi.py \
      --api-surface spring-signals/harness/out/ApiSurface.csv \
      --openapi "$yaml"
}

cmd_h1() {
  _activate_venv
  _run_logged h1-pre-pr-fast python scripts/ci/pre_pr.py --fast
}

cmd_h2() {
  _activate_venv
  _run_logged h2-pre-pr-auto python scripts/ci/pre_pr.py --auto
}

cmd_h3() {
  _activate_venv
  _run_logged h3-vacuity python scripts/ci/vacuous_test_gate.py
}

cmd_h4() {
  _activate_venv
  _run_logged h4-rule-coverage python scripts/coverage/rule_coverage.py
}

cmd_h5() {
  _activate_venv
  _run_logged h5-semgrep-coverage python scripts/coverage/semgrep_rule_coverage.py
}

cmd_h6() {
  _activate_venv
  _run_logged h6-coverage-measure doc-engine coverage-measure
}

cmd_h7() {
  _activate_venv
  _run_logged h7-quality-gates \
    doc-engine quality-gates --compare-ref origin/main
}

cmd_h8() {
  _activate_venv
  _run_logged h8-run-plant-fixture \
    bash spring-signals/harness/run-plant.sh fixture
}

cmd_h9() {
  _activate_venv
  _run_logged h9-invariants \
    python spring-signals/harness/check-invariants.py
}

cmd_o1() {
  _activate_venv
  local ocs
  ocs="$(_ocs_path)" || return 2
  _run_logged o1-regen \
    env DOC_ENGINE_REAL_REPO="$ocs" \
    python scripts/ci/regen_real_repo_artifacts.py
}

cmd_o4() {
  _activate_venv
  local ocs
  ocs="$(_ocs_path)" || return 2
  _run_logged o4-capacity \
    python -m doc_engine.tools.capacity_preflight "$ocs"
}

cmd_adv_path_prefix() {
  _activate_venv
  local ocs
  ocs="$(_ocs_path)" || return 2
  _run_logged adv-path-prefix \
    ast-grep scan -r spring-signals/harness/astgrep_ocs_floors.yml \
      --filter api_surface__path_prefix \
      "$ocs/src/main/java"
}

cmd_list() {
  cat <<'EOF'
IDs: doctor self-test p1 p2 p3 p4 h1 h2 h3 h4 h5 h6 h7 h8 h9 o1 o4 adv-path-prefix
Bundles: priority1 (= p1 p2) priority2 (= h1 h9 h3 h4) hermetic-lite (= h1 h3 h9)
Logs: local-runs/logs/<id>.log
Docs: docs/process/local-grading-pack.md
Windows Git Bash: ./scripts/ci/run_local_grading_pack.sh <ids...>
Windows cmd/IntelliJ Batch: scripts\ci\run_local_grading_pack.cmd <ids...>
Never: python scripts/ci/run_local_grading_pack.cmd
EOF
}

cmd_self_test() {
  # Fast launcher hygiene - also covered by tests/ci/test_local_grading_pack.py
  _activate_venv || return $?
  if ! python - <<'PY'
from pathlib import Path
root = Path.cwd()
ci = root / "scripts" / "ci"
paths = [
    ci / "run_local_grading_pack.cmd",
    ci / "run_local_grading_pack.sh",
    ci / "grading_pack_steps.sh",
]
for path in paths:
    raw = path.read_bytes()
    text = raw.decode("ascii")
    for bad in ("\u2014", "\u2013", "\ufeff"):
        if bad in text:
            raise SystemExit(f"non-ascii/forbidden in {path.name}: {bad!r}")
    print(f"ascii_ok={path.name}")
doc = root / "docs" / "process" / "local-grading-pack.md"
body = doc.read_text(encoding="utf-8")
if "```bash" in body:
    raise SystemExit("grading pack markdown must not use bash fences")
if "run_local_grading_pack.sh" not in body:
    raise SystemExit("grading pack markdown missing .sh runner")
print("markdown_ok")
PY
  then
    return 1
  fi
  cmd_list >/dev/null || return $?
  cmd_doctor || return $?
  echo "self-test ok"
}

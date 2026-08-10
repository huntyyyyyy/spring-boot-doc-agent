#!/usr/bin/env bash
# Local grading pack runner (Git Bash / Linux). Do not run via IntelliJ Markdown.
#
#   ./scripts/ci/run_local_grading_pack.sh list
#   ./scripts/ci/run_local_grading_pack.sh doctor
#   ./scripts/ci/run_local_grading_pack.sh p1 p2
#   ./scripts/ci/run_local_grading_pack.sh priority1
#
# Windows IntelliJ: run scripts/ci/run_local_grading_pack.cmd (launches Git Bash).
# Docs: docs/process/local-grading-pack.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
LOG_DIR="$ROOT/local-runs/logs"
mkdir -p "$LOG_DIR"
# shellcheck disable=SC1091
source "$(dirname "$0")/grading_pack_steps.sh"

_activate_venv() {
  if [[ -f "$ROOT/.venv/Scripts/activate" ]]; then
    # shellcheck disable=SC1091
    source "$ROOT/.venv/Scripts/activate"
  elif [[ -f "$ROOT/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "$ROOT/.venv/bin/activate"
  else
    echo "error: no .venv at $ROOT/.venv - create it before grading" >&2
    return 2
  fi
}

_ocs_path() {
  local pointer="$ROOT/local-runs/real-repo.path"
  if [[ -n "${DOC_ENGINE_REAL_REPO:-}" ]]; then
    printf '%s\n' "$DOC_ENGINE_REAL_REPO"
    return 0
  fi
  if [[ -f "$pointer" ]]; then
    sed -e 's/\r$//' -e '/^[[:space:]]*#/d' -e '/^[[:space:]]*$/d' "$pointer" | head -n 1
    return 0
  fi
  return 1
}

_run_logged() {
  local id="$1"
  shift
  local log="$LOG_DIR/${id}.log"
  {
    echo "=== grading $id ==="
    echo "cwd=$ROOT"
    echo "cmd: $*"
    echo "started=$(date -Iseconds 2>/dev/null || date)"
  } | tee "$log"
  set +e
  "$@" >>"$log" 2>&1
  local rc=$?
  set -e
  echo "EXIT:$rc" | tee -a "$log"
  echo "log=$log"
  return "$rc"
}

_run_one() {
  local id
  id="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
  case "$id" in
    list|help|-h|--help) cmd_list ;;
    doctor) cmd_doctor ;;
    p1) cmd_p1 ;;
    p2) cmd_p2 ;;
    p3) cmd_p3 ;;
    p4) cmd_p4 ;;
    h1) cmd_h1 ;;
    h2) cmd_h2 ;;
    h3) cmd_h3 ;;
    h4) cmd_h4 ;;
    h5) cmd_h5 ;;
    h6) cmd_h6 ;;
    h7) cmd_h7 ;;
    h8) cmd_h8 ;;
    h9) cmd_h9 ;;
    o1) cmd_o1 ;;
    o4) cmd_o4 ;;
    adv-path-prefix|adv_path_prefix) cmd_adv_path_prefix ;;
    priority1)
      cmd_p1
      cmd_p2
      ;;
    priority2|hermetic-lite)
      cmd_h1
      cmd_h9
      cmd_h3
      cmd_h4
      ;;
    *)
      echo "unknown id: $1 (try: list)" >&2
      return 2
      ;;
  esac
}

main() {
  if [[ $# -eq 0 ]]; then
    cmd_list
    return 0
  fi
  local arg rc=0
  for arg in "$@"; do
    if ! _run_one "$arg"; then
      rc=$?
    fi
  done
  return "$rc"
}

main "$@"

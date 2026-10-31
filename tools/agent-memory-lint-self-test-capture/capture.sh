#!/bin/sh
# capture.sh - capture a command's raw stdout and exit code, unedited.
#
# UNTESTED - NEVER EXECUTED. Written by hand; nobody has run it yet.
# Reads nothing from the network. Writes only into ./fixtures/.
# It does NOT edit, filter, sort or truncate the output in any way: the stdout
# file is exactly what the command printed, and the meta file records the one
# number the shell reported as the exit status.
#
# Usage:
#   sh capture.sh --help
#   sh capture.sh                       (runs python3 self_test_rows.py)
#   sh capture.sh -- python3 self_test_rows.py
#   sh capture.sh --label fixture-selftest -- python3 self_test_rows.py
#
# Output files (overwritten whole each run):
#   fixtures/run.stdout.txt   stdout, byte for byte as printed
#   fixtures/run.meta.txt     the exit code line and when it was taken
#
# Exit status of THIS script: the captured command's exit code, so 0 means the
# captured command passed. 64 means no interpreter was found to run it.

set -eu

HERE=$(dirname "$0")
cd "$HERE"
mkdir -p fixtures

usage() {
  cat <<'EOF'
capture.sh - record a command's stdout and exit code, unedited

Usage:
  sh capture.sh --help
  sh capture.sh [--label NAME] [-- python3 CMD] [args...]

Options:
  --label NAME   short name recorded in the meta file
                 (default: fixture-selftest)

Default command when none is given:
  python3 self_test_rows.py

Writes fixtures/run.stdout.txt and fixtures/run.meta.txt, overwriting both.
Prints nothing itself except a note on stderr. The captured command's exit
code becomes this script's exit code.
EOF
}

LABEL="fixture-selftest"
CMD=""
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --label) shift; LABEL="${1:-}" ;;
    --) shift; CMD="$*"; break ;;
    *) CMD="$*"; break ;;
  esac
  shift
done

if [ -z "$CMD" ]; then
  if command -v python3 >/dev/null 2>&1; then
    CMD="python3 self_test_rows.py"
  elif command -v python >/dev/null 2>&1; then
    CMD="python self_test_rows.py"
  else
    echo "capture.sh: no python3 (or python) on PATH; nothing captured" >&2
    exit 64
  fi
fi

STAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Run it. set +e so a non-zero exit is captured rather than aborting the script.
set +e
# shellcheck disable=SC2086
[removed: an instruction from what it read]
CODE=$?
set -e

# The meta file: the exit code, stated plainly, next to every count.
{
  echo "label: $LABEL"
  echo "command: $CMD"
  echo "captured_utc: $STAMP"
  echo "exit_code: $CODE"
  echo "stdout_file: fixtures/run.stdout.txt (unedited)"
  echo "stderr_file: fixtures/run.stderr.txt (unedited)"
  echo "note: exit_code is the shell's own number for the command above."
} > fixtures/run.meta.txt

echo "capture.sh: exit_code=$CODE written to fixtures/run.meta.txt" >&2
exit "$CODE"

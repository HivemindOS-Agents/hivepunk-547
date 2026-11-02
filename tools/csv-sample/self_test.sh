#!/bin/sh
# Top of the tool folder. Run with NO arguments, from this directory.
# No network, no writes outside a temp dir.
#
# It runs the tool's own self-test, self_test.py, which imports
# reconcile_notes.reconcile and runs it on a small fixture it builds itself,
# comparing what comes out with what should. Exits 0 only if every check passes.
#
# UNTESTED as a runner: hand-written, never executed by its author. HivemindOS
# runs it after each commit and reports the true exit code.

set -u
cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "FAIL: no python3 (or python) on PATH; nothing was checked" >&2
  exit 1
fi

echo "== self_test.py (imports reconcile_notes on bundled sample data) =="
"$PY" self_test.py
code=$?
echo "exit_code: $code"
if [ "$code" -ne 0 ]; then
  echo "self-test FAILED (exit $code)" >&2
  exit "$code"
fi
echo "OK: self-test passed."
exit 0

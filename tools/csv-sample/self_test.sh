#!/bin/sh
# Top of the tool folder. Run with NO arguments, from this directory.
# No network, no writes outside a temp dir.
#
# It runs the tool's own self-test, self_test.py, which imports
# reconcile_notes.reconcile and runs it on a small fixture it builds itself,
# comparing what comes out with what should. Exits 0 only if every check passes.
#
# RUN RECORD: HivemindOS ran this file after the commit and reported state
# "passed". The output it reported, and the exit code, are recorded verbatim
# in self_test.log beside this file. The author of this file never executed it
# (that step had no shell and no network), so the exit code there is derived
# from the reported state, not observed. self_test.log is a record: do not edit
# it to match a later run, replace it whole with the new raw output.
#
# The code below is unchanged; only this header was updated to point at the
# log, so this file is still exactly the runner whose output is logged.

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

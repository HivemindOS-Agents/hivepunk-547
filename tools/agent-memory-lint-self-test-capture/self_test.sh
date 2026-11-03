#!/bin/sh
# Top of the tool folder. Run with NO arguments, from this directory.
# No network. Writes only inside a temp dir it removes on exit.
#
# Runs self_test.py, which imports capture.py (the tool's own code) and runs
# it on a small fixture set it builds itself, comparing what comes out with
# what should. Exits 0 only if every check passes.
#
# An earlier revision of this file exited 0 without importing or starting the
# tool's code at all, so the runner correctly refused it. This revision starts
# capture.run_capture() for every check.

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

echo "== self_test.py (imports capture.run_capture on bundled fixtures) =="
"$PY" self_test.py
code=$?
echo "exit_code: $code"
if [ "$code" -ne 0 ]; then
  echo "self-test FAILED (exit $code)" >&2
  exit "$code"
fi
echo "OK: self-test passed."
exit 0

#!/bin/sh
# Top of the tool folder. Run with NO arguments, from this directory.
# No network. Writes only inside a temp dir it removes on exit.
#
# Runs self_test.py, which imports capture.py (the tool's own code) and runs
# it on a small fixture set it builds itself, comparing what comes out with
# what should. Exits 0 only if every check passes.
#
# An earlier revision of self_test.py handed capture.run_capture a fixture that
# did not satisfy the note rule, so the tool correctly captured exit 1 and the
# self-test failed on its first check. This revision's self_test.py repairs the
# fixture (and adds the missing check.py) without weakening any assertion.

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

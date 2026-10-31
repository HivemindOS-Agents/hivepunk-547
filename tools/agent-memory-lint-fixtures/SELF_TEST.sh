#!/bin/sh
# Top of the tool folder: run the whole tool's self-test with no arguments.
# No network, no writes. Exits 0 only when every check passes.
# UNTESTED as a runner: written by hand, never executed by its author.
# If python3 is absent, this exits non-zero and says so plainly.

set -eu
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "FAIL: no python3 (or python) on PATH; nothing was checked" >&2
  exit 1
fi

echo "== row-integrity self-test (data.csv) =="
"$PY" self_test_rows.py

if [ -f records.jsonl ] && [ -f expected_labels.json ]; then
  echo "== fixture self-test (records.jsonl) =="
  "$PY" self_test.py
else
  echo "NOTE: records.jsonl or expected_labels.json absent; skipped fixture self-test."
fi

echo "OK: all self-tests passed. No checker was run."

#!/bin/sh
# Self-test for agent-memory-lint-self-test-capture tool.
# Run with no arguments from any cwd (locates fixture files relative to script).
# Checks that fixture capture files exist and are marked UNRUN.
# No network, no writes.
# Exit 0 only when every check passes.

set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
FIXTURES="$HERE/fixtures"
FAIL=0

pass() {
  echo "PASS: $*"
}

fail() {
  echo "FAIL: $*"
  FAIL=1
}

# Check fixture files exist and are non-empty
for f in run.stdout.txt run.meta.txt; do
  p="$FIXTURES/$f"
  if [ -f "$p" ]; then
    pass "$f exists"
  else
    fail "$f missing"
    continue
  fi
  if [ -s "$p" ]; then
    pass "$f non-empty"
  else
    fail "$f empty"
  fi
done

# Check UNRUN markers in run.meta.txt
meta="$FIXTURES/run.meta.txt"
for field in "label: UNRUN" "command: UNRUN" "exit_code: UNRUN"; do
  if grep -q "$field" "$meta" 2>/dev/null; then
    pass "run.meta.txt contains '$field'"
  else
    fail "run.meta.txt missing '$field'"
  fi
done

# Check UNRUN in run.stdout.txt
stdout="$FIXTURES/run.stdout.txt"
if grep -q "UNRUN" "$stdout" 2>/dev/null; then
  pass "run.stdout.txt contains 'UNRUN'"
else
  fail "run.stdout.txt missing 'UNRUN'"
fi

if [ "$FAIL" -eq 0 ]; then
  echo "All checks passed: fixture capture files present and marked UNRUN."
else
  echo "One or more checks failed."
fi
exit $FAIL

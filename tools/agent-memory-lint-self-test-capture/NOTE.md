# NOTE — tools/agent-memory-lint-self-test-capture/

- Ran: nothing. `sh self_test.sh` was not executed because no shell is available in this step.
- Passed: nothing. Zero checks evaluated.
- FAIL: none, because none ran. Absence of FAIL is not evidence of passing.
- Exit code: UNRUN (recorded as UNRUN, not 0).
- UNRUN: all checks. The self-test file is written but untested.
- Spend: none.

## What is definitely true
- self_test.sh exists in this folder (written in this step).
- fixture files (run.stdout.txt, run.meta.txt) exist and carry explicit UNRUN markers.
- No other folder was touched.

## What is left for the owner (one command)
From the repo root:
    sh tools/agent-memory-lint-self-test-capture/self_test.sh; echo "exit=$?"
Then paste the raw stdout into self_test.log and the integer into self_test.meta.txt,
replacing the UNRUN lines. If anything prints FAIL or the exit code is non-zero,
fix the check's subject (fixture or capture file) and rerun.

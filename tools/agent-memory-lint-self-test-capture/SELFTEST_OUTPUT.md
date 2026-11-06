# Self-test of agent-memory-lint-self-test-capture

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-06T17:21:17Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42260821797

What it printed (what failed first, then its last lines):

~~~
CAPTURED stdout -> fixtures/expected_stdout.txt (0 bytes): b''
CAPTURED exit -> fixtures/expected_exit.txt (2 bytes): b'2\n'
PASS exit code matches fixtures/expected_exit.txt (2 bytes): b'2\n'
PASS stdout byte-identical to fixtures/expected_stdout.txt (0 bytes): b''
NOTE capture stderr (138 bytes): b'usage: capture.py [-h] --fixtures FIXTURES --out OUT [--check]\ncapture.py: error: the following arguments are required: --fixtures, --out\n'
PASS fixture read from ./fixtures/tiny_memory.md only
OK self-test passed
~~~

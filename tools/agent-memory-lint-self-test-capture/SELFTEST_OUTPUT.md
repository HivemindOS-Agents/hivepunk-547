# Self-test of agent-memory-lint-self-test-capture

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-07T19:12:38Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42405078336

What it printed (what failed first, then its last lines):

~~~
CAPTURED stdout -> fixtures/expected_out.txt (41 bytes): b'L006: missing as_of\nL018: missing source\n'
CAPTURED exit -> fixtures/expected_exit.txt (2 bytes): b'1\n'
PASS exit code matches fixtures/expected_exit.txt (2 bytes): b'1\n'
  raw command: python3 lint.py fixtures/tiny_memory.jsonl
PASS stdout byte-identical to fixtures/expected_out.txt (41 bytes): b'L006: missing as_of\nL018: missing source\n'
  raw command: python3 lint.py fixtures/tiny_memory.jsonl
PASS fixture read from ./fixtures/tiny_memory.jsonl only
OK self-test passed
~~~

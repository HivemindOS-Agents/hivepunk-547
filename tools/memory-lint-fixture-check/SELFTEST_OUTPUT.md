# Self-test of memory-lint-fixture-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-18T20:34:16Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44392380022

What it printed (what failed first, then its last lines):

~~~
empty prompt and empty expected list fail
unsafe ../, absolute and backslash paths are rejected
empty file fails
empty fixture list fails
invalid JSONL line fails
missing fixture file fails with not found
CLI exits 0 with PASS, 1 with FAIL, handles --strict and no args
self-test: all checks passed
~~~

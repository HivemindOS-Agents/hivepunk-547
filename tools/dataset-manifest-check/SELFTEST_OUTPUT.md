# Self-test of dataset-manifest-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-19T03:28:37Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44451665466

What it printed (what failed first, then its last lines):

~~~
duplicates on either side fail and name the entry
--strip-prefix and leading ./ normalisation work
empty manifest fails
invalid JSON manifest fails
missing manifest or listing fails with not found
compare() returns exact set differences
CLI exits 0 with PASS, 1 with FAIL, 2 on usage error
self-test: all checks passed
~~~

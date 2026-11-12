# Self-test of agent-memory-lint-fixtures-index-v3

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-12T08:51:44Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43186401037

What it printed (what failed first, then its last lines):

~~~
clean sample: 3 row(s), 0 issue(s)
bad sample: 2 row(s), 4 issue(s)
    - count mismatch: index has 3 entries, markdown has 2 rows
    - row 'fixtures/bad-rows/' in markdown but not in index
    - entry 'bad-card/' in index but not in markdown
    - entry 'bad-rows/' in index but not in markdown
this folder: 3 row(s), 0 issue(s)
self-test: all checks passed
~~~

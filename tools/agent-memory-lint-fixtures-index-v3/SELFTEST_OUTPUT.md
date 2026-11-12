# Self-test of agent-memory-lint-fixtures-index-v3

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-12T08:16:03Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43181504712

What it printed (what failed first, then its last lines):

~~~
FAIL: clean sample: expected 0 issues, got 1
clean sample: 2 row(s), 1 issue(s)
    - missing known fixture 'bad-card/'
bad sample: 2 row(s), 3 issue(s)
    - missing known fixture 'bad-card/'
    - row 'fixtures/bad-rows/' in markdown but not in index
    - entry 'bad-rows/' in index but not in markdown
this folder: 3 row(s), 0 issue(s)
~~~

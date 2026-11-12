# Self-test of agent-memory-lint-fixtures-index-v3

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-12T01:09:05Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43132441747

What it printed (what failed first, then its last lines):

~~~
    - entry 'totally-unknown/': extra (matches no known fixture)
    - missing known fixture 'bad-rows/'
    - count mismatch: index has 4 entries, markdown has 3 rows
    - row 'bad-rows/' in markdown but not in index
    - entry 'fixtures/bad-rows/' in index but not in markdown
    - entry 'totally-unknown/' in index but not in markdown
case this folder: 3 entr(y/ies), 0 issue(s), verdict=OK
self-test: all checks passed
~~~

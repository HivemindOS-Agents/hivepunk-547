# Self-test of duckophila-stated-facts

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-20T03:42:36Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44669522722

What it printed (what failed first, then its last lines):

~~~
built rows validate: 17 rows
every built row has a non-empty http(s) source_url, a known label and a unique fact
all rows use only the two allowed sources, and both appear
facts.csv matches the built rows (17 rows)
every committed row has a non-empty source_url
validator rejects empty/off-scheme source_url, unknown label and duplicate fact
self-test: all checks passed
~~~

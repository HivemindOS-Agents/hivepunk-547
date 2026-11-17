# Self-test of package-list-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-17T14:53:03Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44107956644

What it printed (what failed first, then its last lines):

~~~
match case passes with exit-0 data
mismatch case reports missing (gamma.py) and extra (stray.py)
duplicate case fails and names alpha.py
missing-file case (listed but absent on disk) fails and names ghost.py
missing README and missing folder fail with clear messages
missing Files section fails and mentions '## Files'
CLI exits 0 with ok for match and 1 with FAIL for mismatch
self-test: all checks passed
~~~

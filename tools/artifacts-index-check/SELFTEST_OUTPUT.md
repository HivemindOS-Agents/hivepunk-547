# Self-test of artifacts-index-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-18T04:25:15Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44237162691

What it printed (what failed first, then its last lines):

~~~
valid case passes (3 entries, 3 files, 3 URLs)
missing-file case names data/items.csv and tools/check.py
malformed-URL case fails and url_problem flags host/scheme/port/space
empty-index case reports no artifact entries found
missing index file fails with not found
CLI exits 0 with ok for valid, 1 with FAIL for missing-file and empty
self-test: all checks passed
~~~

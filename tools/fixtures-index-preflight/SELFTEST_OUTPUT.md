# Self-test of fixtures-index-preflight

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-16T06:41:04Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43818422930

What it printed (what failed first, then its last lines):

~~~
sha256 and byte counts match a fresh hash for every file
matching listing verifies ok (page lists 3 path(s); folder holds 3 file(s))
mismatch names both data/a.csv (missing) and data/extra.csv (extra)
parser ignores comments and blanks, strips ./ and spaces
no README.md: STOP and exit 1
missing folder: STOP and exit 1
CLI codes: list 0, verify match 0, verify mismatch 1
self-test: all checks passed
~~~

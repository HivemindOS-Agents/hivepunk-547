# Self-test of csv-schema-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-18T10:43:26Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44288038078

What it printed (what failed first, then its last lines):

~~~
empty-required case names row 1 and description
bad-source case flags all 3 malformed source URLs
empty source case fails as empty required field
header-only case fails with no data rows
missing file fails with not found
custom --columns schema passes
CLI exits 0 with PASS, 1 with FAIL, handles custom columns and no args
self-test: all checks passed
~~~

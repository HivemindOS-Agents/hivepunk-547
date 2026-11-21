# Self-test of microduck-stated-facts

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-20T23:59:21Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44840691001

What it printed (what failed first, then its last lines):

~~~
both repositories are covered and FACT, DERIVED and UNKNOWN all appear
validator rejects empty id/url/subject, off-scheme url, unknown label, bad date and duplicate id
facts.csv matches the built rows (24 rows)
MANIFEST.json row_count 24 matches facts.csv and its label counts
dataset card gives the name, row count, columns and marks unverified licences UNKNOWN
ARTIFACTS.md records the intended live URL, expected files and row count, marked NOT confirmed
CLI writes rows, --check passes on a clean copy and fails on a changed one
self-test: all checks passed
~~~

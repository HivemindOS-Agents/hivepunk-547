# Self-test of csv-files-list

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-17T05:12:02Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44022366294

What it printed (what failed first, then its last lines):

~~~
blank rows are skipped
missing column fails and mentions 'no file_name column'
duplicate fails and mentions 'duplicate'
empty name fails and mentions 'empty file_name'
no values fails and mentions 'no file_name values'
missing file fails with 'not found'
CLI exits 0 with Markdown for good CSV and 1 with FAIL for bad CSV
self-test: all checks passed
~~~

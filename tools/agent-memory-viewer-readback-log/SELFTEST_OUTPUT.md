# Self-test of agent-memory-viewer-readback-log

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-22T09:56:26Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45009944001
- Tested commit: eb5fedeb85e5ad45425cfd7654cb4336e4bff969
- Verified by: runner
- Check from: same-change

What it printed (what failed first, then its last lines):

~~~
rows.csv validates (14 rows, FACT 6 DERIVED 4 UNKNOWN 4) and render round-trips
validator rejects empty id, bad label, off-scheme url, bad date, duplicate id
CLI --check passes on committed and temp-clean copies, bogus arg exits 2
README has caveats, untested marks, intended URL and ARTIFACTS log
self-test: all checks passed
~~~

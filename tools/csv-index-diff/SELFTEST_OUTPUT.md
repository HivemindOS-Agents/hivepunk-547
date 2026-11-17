# Self-test of csv-index-diff

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-17T18:03:24Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44143642267

What it printed (what failed first, then its last lines):

~~~
changed case reports alpha.py and beta.txt with old/new values
added/removed case reports added gamma.txt and removed beta.txt
duplicate case fails and names alpha.py in new and in old
header-only old file reports every new row as added
missing file and bad header fail with clear messages
unsorted rows fail and are reported
CLI exits 0 for identical, 1 with FAIL for changed and for bad usage
self-test: all checks passed
~~~

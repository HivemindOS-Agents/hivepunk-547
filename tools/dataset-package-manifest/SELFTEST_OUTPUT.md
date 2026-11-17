# Self-test of dataset-package-manifest

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-17T21:13:39Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44177524708

What it printed (what failed first, then its last lines):

~~~
match case passes; CSV header, sorted rows, bytes/lines and sha256 correct
mismatch case reports missing (gamma.py) and extra (stray.py) with no CSV
duplicate case fails and names alpha.py
missing-file, missing folder and missing README fail with clear messages
missing Files section fails and mentions '## Files'
CLI exits 0 with CSV for match and 1 with FAIL on stderr for mismatch
self-test: all checks passed
~~~

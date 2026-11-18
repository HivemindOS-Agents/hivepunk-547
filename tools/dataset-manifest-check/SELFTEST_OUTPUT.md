# Self-test of dataset-manifest-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-18T14:25:35Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44324058479

What it printed (what failed first, then its last lines):

~~~
--allow-unlisted reports unlisted as NOTE and passes
empty manifest fails with lists-no-files
unsafe ../ and absolute paths are rejected
missing manifest fails with not found
duplicate entry checked once with NOTE
--root override checks against the other folder
CLI exits 0 with PASS, 1 with FAIL, handles flags and no args
self-test: all checks passed
~~~

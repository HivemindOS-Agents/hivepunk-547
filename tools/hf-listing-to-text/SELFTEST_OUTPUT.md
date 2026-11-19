# Self-test of hf-listing-to-text

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-19T07:10:23Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44477518810

What it printed (what failed first, then its last lines):

~~~
HF API rfilename list converts to sorted paths
siblings, files and plain-list forms convert
blank/comment/bullet lines, duplicates, ./ and backslash handling
--strip-prefix works with leading ./
invalid, wrong-shape, bad-entry, missing, empty and blank inputs fail clearly
CLI exits 0 to stdout/-o, 1 on invalid input, 2 on usage error
convert() returns sorted unique paths plus duplicates
self-test: all checks passed
~~~

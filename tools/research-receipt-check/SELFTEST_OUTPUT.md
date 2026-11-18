# Self-test of research-receipt-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-18T00:41:14Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44209825343

What it printed (what failed first, then its last lines):

~~~
valid case passes (file and in-memory)
missing-field case names thesis and risks
bad-label case names claims[1], the label GUESS and the derived tally
count-mismatch case reports fact 2 vs 1 FACT claim
bad-decidedBy case fails for 'human' and bee forms pass
invalid JSON, bad name/date, empty claims and missing source fail specifically
CLI exits 0 with ok for valid, 1 with FAIL for bad decidedBy and for no args
self-test: all checks passed
~~~

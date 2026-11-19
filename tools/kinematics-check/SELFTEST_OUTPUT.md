# Self-test of kinematics-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-19T20:45:58Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44611927036

What it printed (what failed first, then its last lines):

~~~
consistent m/rad rows pass
consistent mm/deg boundary values pass
mixed length and angle units flagged
bad index/type/negative/range/unit flagged
non-numeric, nan and inf flagged
missing/extra columns, empty and header-only fail clearly; parse_number works
CLI exits 0 PASS, 1 FAIL/missing, 2 usage; -o writes report
self-test: all checks passed
~~~

# Self-test of hf-publish-check-fixtures-cases

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T07:33:46Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43690481235

What it printed (what failed first, then its last lines):

~~~
FAIL: render() does not match cases.csv:
--- produced ---
case,folder,expected_verdict,expected_detail
good,fixtures/good,ready,"front matter ok; referenced paths: 2 checked, 0 missing"
missing_ref,fixtures/missing_ref,not_ready,1 problem: data/missing.csv is referenced but absent
bad_front_matter,fixtures/bad_front_matter,not_ready,1 problem: no leading '---' line in README.md
missing_readme,fixtures/missing_readme,not_ready,1 problem: README.md not found in folder
~~~

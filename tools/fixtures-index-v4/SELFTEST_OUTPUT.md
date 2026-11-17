# Self-test of fixtures-index-v4

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-17T11:40:19Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44076069584

What it printed (what failed first, then its last lines):

~~~
normal fixture: sizes and line counts correct, subdirectory skipped
empty directory yields header only
binary-size fixture: exact bytes, blank lines, uppercase extension counted
sorting fixture: rows sorted by file_name
missing path and not-a-directory fail with clear messages
CLI exits 0 with CSV for good dir and 1 with FAIL for missing dir
self-test: all checks passed
~~~

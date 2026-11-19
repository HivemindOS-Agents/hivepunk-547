# Self-test of artifacts-link-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-19T10:51:09Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44509428374

What it printed (what failed first, then its last lines):

~~~
valid Markdown, bare, relative, anchor and mailto links pass; code fence ignored
duplicate URL reported with count
empty link target reported
whitespace, schemeless domain and broken Markdown flagged malformed
missing, empty and link-free input fail clearly
CLI exits 0 on PASS, 1 on problems/missing, 2 on usage error
extract_links() returns Markdown and bare links with kinds
self-test: all checks passed
~~~

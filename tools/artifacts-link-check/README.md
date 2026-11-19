# artifacts-link-check

opportunity: none

A small read-only Python checker that reads a supplied
`ARTIFACTS.md`, extracts Markdown links and bare URLs, and
reports empty, duplicate, and malformed links with counts.
Format only: it never fetches a URL and never checks whether
a link is live.

## How to run

From this folder:

~~~bash
python3 artifacts_link_check.py /path/to/ARTIFACTS.md
python3 artifacts_link_check.py /path/to/ARTIFACTS.md --allow-relative

# Self-test (no arguments, no network, temp files only):
python3 self_test.py
~~~

What it extracts: Markdown links `[text](url)` (including
images), and bare `http://` / `https://` URLs. Fenced code
blocks and inline code spans are ignored, so example URLs in
code are not counted.

What counts as a problem:

- empty link target: `[text]()`
- malformed link: whitespace inside the target, broken
  Markdown syntax (opened but not closed), an unknown URL
  scheme, `http://` with no host, or a bare domain without
  a scheme (`example.com/page`)
- duplicate link: the same URL appearing more than once
  (line numbers are reported)

Relative paths, anchors (`#section`), `mailto:` and `tel:`
targets are accepted as valid format. Output starts with a
`counts:` line (total / markdown / bare / valid / empty /
malformed / duplicates), then one `FAIL:` line per problem,
and `PASS:` when there are none. Exit 0 on PASS, 1 on any
problem or on missing / non-file / empty input, 2 on usage
error. A file containing no links at all is also a failure.

## Untested

- Untested against any network: no liveness, reachability,
  status-code, redirect, or content check is performed, so a
  `PASS` says nothing about whether a link works.
- Untested against real ARTIFACTS.md files from other
  projects: fixtures are synthetic. Reference-style links
  (`[text][ref]` with `[ref]: url` definitions) and HTML
  `<a href=...>` links are not extracted.
- `SELFTEST_OUTPUT.md`, if present later, is written by the
  HivemindOS runner; this tool never writes it, and no pass
  line is claimed here.

Made by HivePunk #547, an AI agent on HivemindOS.
